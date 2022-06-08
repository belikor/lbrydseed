#!/bin/bash
set -x

OPWD=$(pwd)
APPD=appimgtools

# Change manually as needed
VER=0.9

# Version of Python; it depends on the plugin
PYVER=3.8

# ---------------------------------------------------------------------------
# Download tools
mkdir -p "${APPD}"

# Base AppImage creation tool used by high-level tools
if [ ! -f "${APPD}/appimagetool-x86_64.AppImage" ]
then
    wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O "${APPD}/appimagetool-x86_64.AppImage"
    chmod +x "${APPD}/appimagetool-x86_64.AppImage"
fi

# Higher level tool to create AppImages by using plugins; it already has the base `appimagetool`
if [ ! -f "${APPD}/linuxdeploy-x86_64.AppImage" ]
then
    wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage -O "${APPD}/linuxdeploy-x86_64.AppImage"
    chmod +x "${APPD}/linuxdeploy-x86_64.AppImage"
fi

# Plugin necessary to create AppImages with Python
if [ ! -f "${APPD}/linuxdeploy-plugin-python-x86_64.AppImage" ]
then
    wget https://github.com/niess/linuxdeploy-plugin-python/releases/download/continuous/linuxdeploy-plugin-python-x86_64.AppImage -O "${APPD}/linuxdeploy-plugin-python-x86_64.AppImage"
    chmod +x "${APPD}/linuxdeploy-plugin-python-x86_64.AppImage"
fi

# Alternative.
# AppImage builder to create AppImages from the packages of the operating system
if [ ! -f "${APPD}/appimage-builder-x86_64.AppImage" ]
then
    wget https://github.com/AppImageCrafters/appimage-builder/releases/download/v1.0.0-beta.1/appimage-builder-1.0.0-677acbd-x86_64.AppImage -O "${APPD}/appimage-builder-x86_64.AppImage"
    chmod +x "${APPD}/appimage-builder-x86_64.AppImage"
fi

# "${APPD}/appimage-builder-x86_64.AppImage"

# ---------------------------------------------------------------------------

# The official Python sources are downloaded, compiled, and installed inside
# the `AppDir` directory.
# Make sure necessary compilers and development libraries are available
# before running the `linuxdeploy` command: build-essential, gcc, g++,
# libc6-dev, tk-dev, libxft-dev libxss-dev, libxt-dev, libreadline-dev,
# libbz2-dev, libgdbm-dev, libgdbm-compat-dev

AppDir="${OPWD}/AppDir"

# Create the basic `AppDir` directory, and include the Python interpreter
# with certain packages.
# Include some modules installed by `pip`.
PIP_REQUIREMENTS="requests emoji regex Pillow matplotlib" VERSION=${VER} \
"${APPD}/linuxdeploy-x86_64.AppImage" --appdir "${AppDir}" \
    --plugin python -i "${OPWD}/lbrydseed.svg" -d "${OPWD}/lbrydseed.desktop"

# Produce the final AppImage; it doesn't work well for our case
# so we don't use this option.
#   --output appimage

# Add the necessary `lbrytools` and `lbseed` packages into the `AppDir` directory
sites="${AppDir}/usr/python/lib/python${PYVER}/site-packages"
mkdir -p "${sites}/lbrytools"
cp -r -t "${sites}/lbrytools" "${OPWD}"/lbrytools/*

mkdir -p "${sites}/lbseed"
cp -r -t "${sites}/lbseed" "${OPWD}"/lbseed/*

# Add the executable to the `bin` directory, and create the `AppRun` script
# to call it
mkdir -p "${AppDir}/usr/bin/"
cp "${OPWD}/dseed.py" "${AppDir}/usr/bin"

cat > "${AppDir}/AppRun" <<EOF
#!/bin/sh

if [ -z "\${APPDIR+x}" ]
then
    echo Run outside of AppImage
    APPDIR="\$(dirname "\$0")"
fi

"\${APPDIR}/usr/bin/python3" "\${APPDIR}/usr/bin/dseed.py"
EOF

chmod +x "${AppDir}/AppRun"

# Icon needed for the window
cp "${OPWD}/lbrydseed.png" "${AppDir}/usr/bin/"

# Produce the final AppImage if the `AppDir` directory has everything it needs
"${APPD}/appimagetool-x86_64.AppImage" "${AppDir}" "${OPWD}/lbrydseed-${VER}-x86_64.AppImage"
