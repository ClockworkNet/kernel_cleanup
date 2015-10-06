# kernel_cleanup

Evaluate installed Linux kernel packages (linux-headers, linux-image, linux-image-extra) and purge any that are not the current version or the newest version.


## Cron Example

```
@daily /usr/local/sbin/kernel_cleanup -q
```


## Compatibility

Tested on:

- Ubuntu 10.04 (Lucid Lynx)
- Ubuntu 12.04 (Precise Pangolin)
- Ubuntu 14.04 (Trusty Tahr)


## License

- [LICENSE](LICENSE) [MIT License](http://www.opensource.org/licenses/MIT)
