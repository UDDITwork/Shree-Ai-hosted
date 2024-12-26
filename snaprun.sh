#!/bin/bash

# This script is used to run the app in the snap environment
# export QTWEBENGINE_DISABLE_GPU=1
# export QTWEBENGINE_CHROMIUM_FLAGS="--enable-logging --log-level=0 --v=1"

case "$SNAP_ARCH" in
    "amd64") ARCH='x86_64-linux-gnu'
    ;;
    "i386") ARCH='i386-linux-gnu'
    ;;
    *)
        echo "Unsupported architecture for this app build"
        exit 1
    ;;
esac

export QTWEBENGINEPROCESS_PATH=$SNAP/lib/python3.10/site-packages/PySide6/Qt/libexec/QtWebEngineProcess

# nvidia drivers fix
export LIBGL_DRIVERS_PATH=$SNAP/usr/lib/$ARCH/dri
if [ -e "/var/lib/snapd/lib/gl/xorg/nvidia_drv.so" ]; then
    export LIBGL_DRIVERS_PATH=/var/lib/snapd/lib/gl/xorg
    export LD_LIBRARY_PATH=/var/lib/snapd/lib/gl:$LD_LIBRARY_PATH
else
    export LIBGL_DRIVERS_PATH=$SNAP/usr/lib/$ARCH/dri
fi

python3 $SNAP/src/pygpt_net/app.py "$@"