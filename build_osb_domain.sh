# BUILD THE IMAGE (replace all environment variables)
NOCACHE=true
BUILD_START=$(date '+%s')
docker build --network mydocker_default --force-rm=$NOCACHE --no-cache=true -t osb_domain -f osb-domain/myDockerfile_osb_domain . || {
  echo "There was an error building the image."
  exit 1
}

BUILD_END=$(date '+%s')
BUILD_ELAPSED=`expr $BUILD_END - $BUILD_START`
