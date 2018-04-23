#!/usr/bin/env bash

# merge-external-schemas.sh: Pull down the external repositories and
# merge their schemas directories and the contents of the ztag directory
# in an external folder (by default, build/schemas-merged).

set -e

SCHEMAS_OUTPUT=${SCHEMAS_OUTPUT:-"build/schemas-merged"}
GIT_REPO_ROOT=${GIT_REPO_ROOT:-"build/schemas-git"}
ZCRYPTO_CLONE_DIR=${ZCRYPTO_CLONE_DIR:-"$GIT_REPO_ROOT/zcrypto"}
ZGRAB2_CLONE_DIR=${ZGRAB2_CLONE_DIR:-"$GIT_REPO_ROOT/zgrab2"}
ZCRYPTO_SKIP_PULL=${ZCRYPTO_SKIP_PULL:-"false"}
ZGRAB2_SKIP_PULL=${ZGRAB2_SKIP_PULL:-"false"}
ZTAG_ROOT=${ZTAG_ROOT:-"$(dirname $0)/ztag"}

if ! [ -d "$SCHEMAS_OUTPUT" ]; then
    echo "Creating merged schema output directory '$SCHEMAS_OUTPUT'..."
    mkdir -p "$SCHEMAS_OUTPUT"
else
    if [[ "$1" == "-f" ]]; then
        echo "Ignoring already-existing SCHEMAS_OUTPUT folder '$SCHEMAS_OUTPUT'..."
    else    
        echo "ERROR: Schema output folder $SCHEMAS_OUTPUT already exists. Remove it or set SCHEMAS_OUTPUT to a different path then retry, or run '$0 -f' to ignore it."
        exit 1
    fi
fi

if ! [ -d "$ZCRYPTO_CLONE_DIR" ]; then
    echo "Cloning zcrypto into '$ZCRYPTO_CLONE_DIR'..."
    set -x
    git clone "https://github.com/zmap/zcrypto" "$ZCRYPTO_CLONE_DIR"
    set +x
    ZCRYPTO_SKIP_PULL="true"
fi

if ! [ -d "$ZGRAB2_CLONE_DIR" ]; then
    echo "Cloning zgrab2 into '$ZGRAB2_CLONE_DIR'..."
    set -x
    git clone "https://github.com/zmap/zgrab2" "$ZGRAB2_CLONE_DIR"
    set +x
    ZGRAB2_SKIP_PULL="true"
fi

if ! [ -z "$ZCRYPTO_BRANCH" ]; then
    # If not set, just leave it as-is
    echo "Checking out $ZCRYPTO_BRANCH in $ZCRYPTO_CLONE_DIR..."
    set -x
    pushd "$ZCRYPTO_CLONE_DIR"
    git checkout "$ZCRYPTO_BRANCH"
    popd
    set +x
fi

if ! [ -z "$ZGRAB2_BRANCH" ]; then
    echo "Checking out $ZGRAB2_BRANCH in $ZGRAB2_CLONE_DIR..."
    set -x
    pushd "$ZGRAB2_CLONE_DIR"
    git checkout "$ZGRAB2_BRANCH"
    popd
    set +x
fi

if [[ "$ZCRYPTO_SKIP_PULL" == "false" ]]; then
    echo "Running 'git pull' in $ZCRYPTO_CLONE_DIR..."
    set -x
    pushd "$ZCRYPTO_CLONE_DIR"
    git pull
    popd
    set +x
else
    echo "Skipping 'git pull' in $ZCRYPTO_CLONE_DIR."
fi

if [[ "$ZGRAB2_SKIP_PULL" == "false" ]]; then
    echo "Running 'git pull' in $ZGRAB2_SKIP_PULL..."
    set -x
    pushd "$ZGRAB2_CLONE_DIR"
    git pull
    popd
    set +x
else
    echo "Skipping 'git pull' in $ZGRAB2_CLONE_DIR."
fi

if ! [ -f "$ZCRYPTO_CLONE_DIR/schemas/zcrypto.py" ]; then
    echo "Bad ZCRYPTO_CLONE_DIR '$ZCRYPTO_CLONE_DIR': could not find zcrypto.py"
    exit 2
fi


if ! [ -f "$ZGRAB2_CLONE_DIR/schemas/zgrab2/__init__.py" ]; then
    echo "Bad ZGRAB2_CLONE_DIR '$ZGRAB2_CLONE_DIR': could not find schemas/zgrab2/__init__.py"
    exit 2
fi

echo "Copying schemas into $SCHEMAS_OUTPUT..."
set -x
cp -r $ZCRYPTO_CLONE_DIR/schemas "$SCHEMAS_OUTPUT"
cp -r $ZGRAB2_CLONE_DIR/schemas "$SCHEMAS_OUTPUT"
cp -r "$ZTAG_ROOT" "$SCHEMAS_OUTPUT/schemas"
set +x

echo "Creating $SCHEMAS_OUTPUT/schemas/__init__.py..."
touch "$SCHEMAS_OUTPUT/schemas/__init__.py"

echo "Done -- update PYTHONPATH to include '$SCHEMAS_OUTPUT':"
echo "export PYTHONPATH=\$PYTHONPATH;$SCHEMAS_OUTPUT"

