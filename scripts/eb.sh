#!/bin/bash
set -e

rm -rf /var/tmp/portage/media-libs/x264-0.0.20190903-r1  || true
rm -rf /var/tmp/portage/media-video/x264-encoder-0.0.20190903 || true

ls -lh /var/lib/layman/lto-overlay/sys-config/ltoize/files/

# echo -e "\n\n### media-video/x264-encoder"
# ebuild /usr/portage/media-video/x264-encoder/x264-encoder-0.0.20190903.ebuild prepare
# cd /var/tmp/portage/media-video/x264-encoder-0.0.20190903/work/x264-snapshot-20190903-2245
# cat /home/iphands/prog/gentooLTO/sys-config/ltoize/files/patches/media-video/x264-encoder/lto.patch | patch -p1

echo -e "\n\n### media-libs/x264"
ebuild /usr/portage/media-libs/x264/x264-0.0.20190903-r1.ebuild prepare
cd /var/tmp/portage/media-libs/x264-0.0.20190903-r1/work/x264-snapshot-20190903-2245
# cat /home/iphands/prog/gentooLTO/sys-config/ltoize/files/patches/media-libs/x264/lto.patch | patch -p1
