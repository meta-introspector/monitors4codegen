export GUILE_LOAD_PATH=...:${HOME}/.guix-profile/share/guile/site/3.0:$GUILE_LOAD_PATH
export GUILE_LOAD_COMPILED_PATH=...:${HOME}/.guix-profile/lib/guile/3.0/site-ccache:$GUILE_LOAD_COMPILED_PATH
. venv_monitors4codegen/bin/activate
python ./test_scheme.py
