# BUILD THE IMAGE (replace all environment variables)
NOCACHE=true
BUILD_START=$(date '+%s')
docker build --network mynet --force-rm=$NOCACHE --no-cache=false -t oracle/osb_domain:12.2.1.0 -f Dockerfile_osb_domain . || {
  echo "There was an error building the image."
  exit 1
}

BUILD_END=$(date '+%s')
BUILD_ELAPSED=`expr $BUILD_END - $BUILD_START`
