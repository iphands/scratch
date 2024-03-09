#!/bin/bash -ex
set -e


date=`date "+%Y-%m-%dT%H_%M_%S"`
BACKUP_ROOT="/mnt/noir/bak/cosmo/gentoo"

bak() {
  SOURCE=$1
  LABEL=$2

  if [[ "$SOURCE" == "" ]]
  then
    echo BAD SOURCE
    exit 1
  fi

  if [[ "$LABEL" == "" ]]
  then
    echo BAD SOURCE
    exit 1
  fi

  mkdir -p /mnt/${LABEL}
  mount $SOURCE -o bind /mnt/${LABEL}
  mkdir -p ${BACKUP_ROOT}/cosmo/${LABEL}
  cd ${BACKUP_ROOT}/cosmo/${LABEL}/
  THIS=$PWD
  rm -rf current incomplete_back*
  ln -s initial current
  CURR=`readlink ./current`
  rsync -xHAEptavPS --delete --delete-excluded --exclude-from=${BACKUP_ROOT}/excludes --link-dest=${THIS}/${CURR} /mnt/${LABEL} incomplete_back-$date
  mv incomplete_back-$date back-$date
  rm -f current
  ln -s back-$date current
  sync

}

time bak / rootfs
time bak /home home
