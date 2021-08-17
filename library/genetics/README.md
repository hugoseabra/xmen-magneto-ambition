# Genetics Library

This library was developed so support a way to find out whether a DNA is mutant.
So, it is important to understand the keywords to manage the domain artifacts.

## Glossary

### Amino acids

The sequence of the bases (genetic instructions) contained inside a DNA. Those
instructions, placed on a certain sequence, determine our unique genetic code
and provides the instructions for producing molecules in the body.

A, C, G, and T are the "letters" of the DNA code. They stand for the chemicals
adenine (A), cytosine (C), guanine (G), and thymine (T), respectively,
that make up the nucleotide bases of DNA.

### Codon

Codon is a simple conjunction of 2 or 3 nucleic (amino acid) groups. It is named
a tripled code. Each DNA usually has 6 pairs of Codons, each one separated in
two groups of 3. In other words, for simplicity purposes, our comprehension
of a DNA is that it must have 6 sequences of codon pairs (6 letters each).

### DNA - Deoxyribonucleic Acid

Deoxyribonucleic acid, more commonly known as DNA, is a complex molecule that
contains all of the information necessary to build and maintain an organism.

# Architecture

In this library we defined a state for each model described above on the following way:

## The Amino Acid Enum

An **enum** implemented to restrict the usage of the supported letters. Any
other letter would raise a warning telling  

### The Codon Pair Interface

It is a structure way to unique two groups of codon inside a predictable and
reliable state of object. With a good support to keep sequence of the codes,
we can retrieve the genetic sequence and compare whether an external given sequence
is equals the existing one.

### The DNA Interface

An object which will support exactly 6 pairs of codon pairs. While the codon
pairs are added to the object, it is not valid and cannot be used for comparisons.

Once the DNA is valid, we work on the pre-processed states to ease comparions with
other DNAs. The comparisons can be done comparting a sequence of codes of a codon
pair (6 letters) to the sequence inside a DNA. It can be done in the following
sequence:

- **Horizontally:** from left to right, line by line;
- **Vertically:** from top to bottom, column by column;
- **Obliquely:** from top-left to bottom-right and from bottom-left to top-right;

Once that we find sequence matches the sequence of genetic sequence contained
inside the DNA, we say that it **matches** the sequence.

# The Analyser Interface

The analyser supports a reference of how a mutant DNA is like, but keeping
internally an instance with the genetic sequence of a mutant DNA.

What this object does is to find out whether a given DNA is mutant but checking
two or more matches to mutant DNA. If so, we say that the give DNA is mutant.

