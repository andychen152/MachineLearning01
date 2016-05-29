CXX=g++

BINARIES = Main

all: ${BINARIES}

tests: ${BINARIES}
#	./Main training.txt testing.txt

Main: triclassify.o MyClass.o TestClass.o
	${CXX} $^ -o $@

clean:
	/bin/rm -f ${BINARIES} *.o

clean2:
	/bin/rm -f ${BINARIES} *~

#cleandb:
#	/bin/rm -f ${BINARIES} profile_database.txt
