import click
import shodan

from operator import itemgetter
from shodan.cli.helpers import get_api_key


@click.group()
def alert():
    """Manage the network alerts for your account"""
    pass


@alert.command(name='clear')
def alert_clear():
    """Remove all alerts"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        alerts = api.alerts()
        for alert in alerts:
            click.echo(u'Removing {} ({})'.format(alert['name'], alert['id']))
            api.delete_alert(alert['id'])
    except shodan.APIError as e:
        raise click.ClickException(e.value)
    click.echo("Alerts deleted")


@alert.command(name='create')
@click.argument('name', metavar='<name>')
@click.argument('netblocks', metavar='<netblocks>', nargs=-1)
def alert_create(name, netblocks):
    """Create a network alert to monitor an external network"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        alert = api.create_alert(name, netblocks)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho('Successfully created network alert!', fg='green')
    click.secho('Alert ID: {}'.format(alert['id']), fg='cyan')


@alert.command(name='info')
@click.argument('alert', metavar='<alert id>')
def alert_info(alert):
    """Show information about a specific alert"""
    key = get_api_key()
    api = shodan.Shodan(key)

    try:
        info = api.alerts(aid=alert)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho(info['name'], fg='cyan')
    click.secho('Created: ', nl=False, dim=True)
    click.secho(info['created'], fg='magenta')

    click.secho('Notifications: ', nl=False, dim=True)
    if 'triggers' in info and info['triggers']:
        click.secho('enabled', fg='green')
    else:
        click.echo('disabled')

    click.echo('')
    click.secho('Network Range(s):', dim=True)

    for network in info['filters']['ip']:
        click.echo(u' > {}'.format(click.style(network, fg='yellow')))

    click.echo('')
    if 'triggers' in info and info['triggers']:
        click.secho('Triggers:', dim=True)
        for trigger in info['triggers']:
            click.echo(u' > {}'.format(click.style(trigger, fg='yellow')))
        click.echo('')


@alert.command(name='list')
@click.option('--expired', help='Whether or not to show expired alerts.', default=True, type=bool)
def alert_list(expired):
    """List all the active alerts"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        results = api.alerts(include_expired=expired)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    if len(results) > 0:
        click.echo(u'# {:14} {:<21} {:<15s}'.format('Alert ID', 'Name', 'IP/ Network'))

        for alert in results:
            click.echo(
                u'{:16} {:<30} {:<35} '.format(
                    click.style(alert['id'], fg='yellow'),
                    click.style(alert['name'], fg='cyan'),
                    click.style(', '.join(alert['filters']['ip']), fg='white')
                ),
                nl=False
            )

            if 'triggers' in alert and alert['triggers']:
                click.secho('Triggers: ', fg='magenta', nl=False)
                click.echo(', '.join(alert['triggers'].keys()), nl=False)

            if 'expired' in alert and alert['expired']:
                click.secho('expired', fg='red')
            else:
                click.echo('')
    else:
        click.echo("You haven't created any alerts yet.")


@alert.command(name='remove')
@click.argument('alert_id', metavar='<alert ID>')
def alert_remove(alert_id):
    """Remove the specified alert"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        api.delete_alert(alert_id)
    except shodan.APIError as e:
        raise click.ClickException(e.value)
    click.echo("Alert deleted")


@alert.command(name='triggers')
def alert_list_triggers():
    """List the available notification triggers"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        results = api.alert_triggers()
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    if len(results) > 0:
        click.secho('The following triggers can be enabled on alerts:', dim=True)
        click.echo('')

        for trigger in sorted(results, key=itemgetter('name')):
            click.secho('{:<12} '.format('Name'), dim=True, nl=False)
            click.secho(trigger['name'], fg='yellow')

            click.secho('{:<12} '.format('Description'), dim=True, nl=False)
            click.secho(trigger['description'], fg='cyan')

            click.secho('{:<12} '.format('Rule'), dim=True, nl=False)
            click.echo(trigger['rule'])

            click.echo('')
    else:
        click.echo("No triggers currently available.")


@alert.command(name='enable')
@click.argument('alert_id', metavar='<alert ID>')
@click.argument('trigger', metavar='<trigger name>')
def alert_enable_trigger(alert_id, trigger):
    """Enable a trigger for the alert"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        api.enable_alert_trigger(alert_id, trigger)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho('Successfully enabled the trigger: {}'.format(trigger), fg='green')


@alert.command(name='disable')
@click.argument('alert_id', metavar='<alert ID>')
@click.argument('trigger', metavar='<trigger name>')
def alert_disable_trigger(alert_id, trigger):
    """Disable a trigger for the alert"""
    key = get_api_key()

    # Get the list
    api = shodan.Shodan(key)
    try:
        api.disable_alert_trigger(alert_id, trigger)
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    click.secho('Successfully disabled the trigger: {}'.format(trigger), fg='green')
