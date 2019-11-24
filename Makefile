# RUNTEST=python -m unittest -v -b
# ALLMODULES=$(patsubst %.py, %, $(wildcard test_*.py))

# default: clean package

# clean:
# 	rm -f plugin.video.cgtn-0.0.2.zip

# package:
# 	cd .. ; zip plugin.video.cgtn/plugin.video.cgtn-0.0.2.zip -@ < plugin.video.cgtn/package.lst ; cp plugin.video.cgtn/plugin.video.cgtn-0.0.2.zip ~/

# all:
# 	${RUNTEST} ${ALLMODULES}

# % : test_%.py
# 	${RUNTEST} test_$@

RUNTEST=python -m unittest -v -b
ALLMODULES=$(patsubst %.py, %, $(wildcard test_*.py))

all:
	${RUNTEST} ${ALLMODULES}

% : test_%.py
	${RUNTEST} test_$@