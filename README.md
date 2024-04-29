# DTU-02180-Group-44-BeliefProject


### About the project
The project is part of the course [02180 Introduction to Artificial Intelligence](http://kurser.dtu.dk/course/2023-2024/02180) of DTU.

* **Entailment check**:  
  Based on the `PL-Resolution` algorithm in the book "[Artificial Intelligence: A Modern Approach]https://aima.cs.berkeley.edu/global-index.html" by Stuart Russell and Peter Norvig.

  ### Authors

* [Thomas Jerver Asmussen](https://github.com/ThomasAsmussen) (s203828)
* [Martin Schaarup](https://github.com/fast2day) (s203851)
* [Jonatan Jais Kofoed Rasmussen](https://github.com/JonatanRasmussen) (s183649)
* [Rasmus Porsgaard](https://github.com/RallTheManiac)(s203953)


### Project structure
* `BeliefsByThomas.py`: Runs the main script which consists of everything from the belief base to the menu.

### Installation

To install the required libraries, run:
```bash
$ pip install sympy
```

### Usage

The engine can be used through the mainscript `BeliefsByThomas.py`

#### Example of usage
```
Belief Revision Engine
1. Show Belief Base
2. Add Formula to Belief Base     
3. Remove Formula from Belief Base
4. Check Formula Entailment       
5. Exit
Enter choice (1-5): 2

Formula Syntax Guide:     
Logical Operators Allowed:
  ! : NOT
  & : AND
  | : OR
  -> : IMPLICATION (use as a->b for a implies b)
  <-> : BICONDITIONAL (use as a<->b for a if and only if b)
Use parentheses to group expressions as needed.
Enter a formula to add to the belief base: a->b
Added 'a->b' to the belief base.
Formula added successfully.

Belief Revision Engine
1. Show Belief Base
2. Add Formula to Belief Base
3. Remove Formula from Belief Base
4. Check Formula Entailment
5. Exit
Enter choice (1-5): 2

Formula Syntax Guide:
Logical Operators Allowed:
  ! : NOT
  & : AND
  | : OR
  -> : IMPLICATION (use as a->b for a implies b)
  <-> : BICONDITIONAL (use as a<->b for a if and only if b)
Use parentheses to group expressions as needed.
Enter a formula to add to the belief base: !b
Added '!b' to the belief base.
Formula added successfully.

Belief Revision Engine
1. Show Belief Base
2. Add Formula to Belief Base
3. Remove Formula from Belief Base
4. Check Formula Entailment
5. Exit
Enter choice (1-5): 1
Current Belief Base: {'a->b', '!b'}
```

### License

```
The MIT License (MIT)

Copyright (c) 2024 Thomas Jerver Asmussen, Martin Schaarup, Jonatan Jais Koefoed Rasmussen, Rasmus Porsgaard

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```