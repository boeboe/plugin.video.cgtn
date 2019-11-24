RUNTEST=python -m unittest -v -b
ALLMODULES=$(patsubst %.py, %, $(wildcard test_*.py))
VERSION=0.0.3

default: clean package

clean:
	rm -f plugin.video.cgtn-${VERSION}.zip

package:
	cd .. ; zip plugin.video.cgtn/plugin.video.cgtn-${VERSION}.zip -@ < plugin.video.cgtn/package.lst ; cp plugin.video.cgtn/plugin.video.cgtn-${VERSION}.zip ~/

# all:
# 	${RUNTEST} ${ALLMODULES}

# % : test_%.py
# 	${RUNTEST} test_$@

# RUNTEST=python -m unittest -v -b
# ALLMODULES=$(patsubst %.py, %, $(wildcard test_*.py))

# all:
# 	${RUNTEST} ${ALLMODULES}

# % : test_%.py
# 	${RUNTEST} test_$@