Systemd configuration
----------------------

.. note::

    All the command lines below should be executed as root.

Systemd offers a convenient way to manage your Funkwhale instance if you're
not using docker.

We'll see how to setup systemd to properly start a Funkwhale instance.

First, download the sample unitfiles:

.. parsed-literal::

    curl -L -o "/etc/systemd/system/funkwhale.target" "https://dev.funkwhale.audio/funkwhale/funkwhale/raw/|version|/deploy/funkwhale.target"
    curl -L -o "/etc/systemd/system/funkwhale-server.service" "https://dev.funkwhale.audio/funkwhale/funkwhale/raw/|version|/deploy/funkwhale-server.service"
    curl -L -o "/etc/systemd/system/funkwhale-worker.service" "https://dev.funkwhale.audio/funkwhale/funkwhale/raw/|version|/deploy/funkwhale-worker.service"
    curl -L -o "/etc/systemd/system/funkwhale-beat.service" "https://dev.funkwhale.audio/funkwhale/funkwhale/raw/|version|/deploy/funkwhale-beat.service"

This will download three unitfiles:

- ``funkwhale-server.service`` to launch the Funkwhale web server
- ``funkwhale-worker.service`` to launch the Funkwhale task worker
- ``funkwhale-beat.service`` to launch the Funkwhale task beat (this is for recurring tasks)
- ``funkwhale.target`` to easily stop and start all of the services at once

You can of course review and edit them to suit your deployment scenario
if needed, but the defaults should be fine.

Once the files are downloaded, reload systemd:

.. code-block:: shell

    systemctl daemon-reload

And start the services:

.. code-block:: shell

    systemctl start funkwhale.target

To ensure all Funkwhale processes are started automatically after a reboot, run:

.. code-block:: shell
    
    systemctl enable funkwhale-server
    systemctl enable funkwhale-worker
    systemctl enable funkwhale-beat

You can check the statuses of all processes like this:

.. code-block:: shell

    systemctl status funkwhale-\*
