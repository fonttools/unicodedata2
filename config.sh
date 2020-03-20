# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]

function pre_build {
    # Any stuff that you need to do before you start building the wheels
    # Runs in the root directory of this repository.
    :
}

function run_tests {
    # The function is called from an empty temporary directory.
    cd ..

    # check we have the expected version and architecture for Python
    python -c "import sys; print(sys.version)"
    python -c "import struct; print(struct.calcsize('P') * 8)"

    # Get absolute path to the pre-compiled wheel
    wheelhouse=$(abspath wheelhouse)
    wheel=$(ls ${wheelhouse}/unicodedata2*.whl | head -n 1)
    if [ ! -e "${wheel}" ]; then
        echo "error: can't find wheel in ${wheelhouse} folder" 1>&2
        exit 1
    fi

    # Install pre-compiled wheel and run tests against it
    tox --installpkg "${wheel}"
}
