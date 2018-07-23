# Generated by Django 2.0.6 on 2018-07-22 16:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommandLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True, verbose_name='date time')),
                ('command', models.CharField(max_length=255, verbose_name='command')),
            ],
            options={
                'ordering': ['-datetime'],
                'permissions': (('can_view_command_log', 'Can view command log info'),),
            },
        ),
        migrations.CreateModel(
            name='CommandsSequence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Task name')),
                ('commands', models.TextField(verbose_name='Task commands')),
            ],
            options={
                'permissions': (('can_add_commandssequence', 'Can add commands'), ('can_change_commandssequence', 'Can change commands info'), ('can_delete_commandssequence', 'Can delete commands info'), ('can_view_commandssequence', 'Can view commands info'), ('can_execute_commandssequence', 'Can execute commands')),
            },
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Credential name')),
                ('username', models.CharField(max_length=40, verbose_name='Auth user name')),
                ('port', models.PositiveIntegerField(default=22, verbose_name='Port')),
                ('method', models.CharField(choices=[('password', 'password'), ('key', 'key')], default='password', max_length=40, verbose_name='Method')),
                ('key', models.TextField(blank=True, verbose_name='Key')),
                ('password', models.CharField(blank=True, max_length=40, verbose_name='Password')),
                ('proxy', models.BooleanField(default=False, verbose_name='Proxy')),
                ('proxyserverip', models.GenericIPAddressField(blank=True, null=True, protocol='ipv4', verbose_name='Proxy ip')),
                ('proxyport', models.PositiveIntegerField(blank=True, null=True, verbose_name='Proxy port')),
                ('proxypassword', models.CharField(blank=True, max_length=40, verbose_name='Proxy password')),
                ('protocol', models.CharField(choices=[('ssh-password', 'ssh-password'), ('ssh-key', 'ssh-key'), ('ssh-key-with-password', 'ssh-key-with-password'), ('vnc', 'vnc'), ('rdp', 'rdp'), ('telnet', 'telnet')], default='ssh-password', max_length=40, verbose_name='Protocol')),
                ('width', models.PositiveIntegerField(default=1024, verbose_name='width')),
                ('height', models.PositiveIntegerField(default=768, verbose_name='height')),
                ('dpi', models.PositiveIntegerField(default=96, verbose_name='dpi')),
                ('security', models.CharField(choices=[('rdp', 'Standard RDP encryption'), ('nla', 'Network Level Authentication'), ('tls', 'TLS encryption'), ('any', 'Allow the server to choose the type of security')], default='any', max_length=40, verbose_name='Security')),
            ],
            options={
                'permissions': (('can_add_credential', 'Can add credential'), ('can_change_credential', 'Can change credential info'), ('can_delete_credential', 'Can delete credential info'), ('can_view_credential', 'Can view credential info')),
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_time', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='End time')),
                ('channel', models.CharField(editable=False, max_length=100, unique=True, verbose_name='Channel name')),
                ('log', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Log name')),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='Start time')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Is finished')),
                ('width', models.PositiveIntegerField(default=90, verbose_name='Width')),
                ('height', models.PositiveIntegerField(default=40, verbose_name='Height')),
                ('gucamole_client_id', models.CharField(blank=True, editable=False, max_length=100, verbose_name='Gucamole channel name')),
            ],
            options={
                'ordering': ['-start_time'],
                'permissions': (('can_delete_log', 'Can delete log info'), ('can_view_log', 'Can view log info'), ('can_play_log', 'Can play record')),
            },
        ),
        migrations.CreateModel(
            name='ServerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatedatetime', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='Update time')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Server group name')),
                ('createdatetime', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
            ],
            options={
                'permissions': (('can_add_servergroup', 'Can add group'), ('can_change_servergroup', 'Can change group info'), ('can_delete_servergroup', 'Can delete group info'), ('can_view_servergroup', 'Can view group info')),
            },
        ),
        migrations.CreateModel(
            name='ServerInfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatedatetime', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='Update time')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='Server name')),
                ('hostname', models.CharField(blank=True, max_length=40, verbose_name='Host name')),
                ('ip', models.GenericIPAddressField(protocol='ipv4', verbose_name='ip')),
                ('createdatetime', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('credential', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Credential')),
            ],
            options={
                'permissions': (('can_add_serverinfo', 'Can add server'), ('can_change_serverinfo', 'Can change server info'), ('can_delete_serverinfo', 'Can delete server info'), ('can_connect_serverinfo', 'Can connect to server'), ('can_kill_serverinfo', 'Can kill online user'), ('can_monitor_serverinfo', 'Can monitor user action'), ('can_view_serverinfo', 'Can view server info'), ('can_filemanage_serverinfo', 'Can manage file')),
            },
        ),
        migrations.AddField(
            model_name='servergroup',
            name='servers',
            field=models.ManyToManyField(related_name='servers', to='common.ServerInfor', verbose_name='Servers'),
        ),
        migrations.AddField(
            model_name='log',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.ServerInfor', verbose_name='Server'),
        ),
    ]
