# umengpush

umengpush是一个友盟push的封装，清晰地定了如何使用python 调用umeng push api.

# Getting started

Here is a simple example orm operation for Dbskit:

````python

    # coding=utf-8
    from umengpush.ios import UmengIosPush
    from umengpush.android import UmengAndroidPush
    from umengpush import UmengPush

    up = UmengPush(delegator_cls=UmengIosPush)

    help(up.directedcast)

    help(up.broadcast)

    help(up.groupcast)

    help(up.customizedcast)

    help(up.filecast)
    
````

## Documentation

    TODO

## Discussion and support

Report bugs on the *GitHub issue tracker <https://github.com/listen-lavender/umengpush/issues*. 