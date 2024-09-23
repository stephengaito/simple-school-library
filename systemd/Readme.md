# Installing the Simple-School-Library using systemd

Make a correct copy of the `schoolLib.service` by copying
`schoolLib.service.example` and editing it as needed.

Move you new `schoolLib.service` to the `/etc/systemd/system` directory.

Type:

```
sudo systemctl enable schoolLib.service
```

Then you can either type:
```
sudo systemctl start schoolLib.service
```
OR simply reboot your computer
