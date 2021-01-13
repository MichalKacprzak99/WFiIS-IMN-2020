CXX=g++
OUTPUT=main
CXXFLAGS= -O2
SRC=$(wildcard *.cpp)
OBJ=$(SRC:.cpp=.o)

$(OUTPUT): $(OBJ)
	$(CXX) $? -o $@

$(OBJ): $(SRC)
	$(CXX) $(CXXFLAGS) -c $*.cpp -o $@

.PHONY: clean run rebuild val 

clean:
	rm -f *.o
	cd data && rm -f *.dat
	cd images && rm -f *.png
	rm -f $(OUTPUT) $(OBJ)

run: $(OUTPUT)
	./$(OUTPUT)
	gnuplot plot.sh

rebuild: 
	make clean
	make run	

val:
	valgrind ./$(OUTPUT)
