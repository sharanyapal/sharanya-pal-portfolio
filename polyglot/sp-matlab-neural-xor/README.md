# MATLAB / XOR Neural Network From Scratch

End-to-end vectorized backpropagation with a tanh hidden layer, sigmoid output, binary cross-entropy, and momentum SGD. Architecture 2 → 8 → 1, trained on XOR without any ML toolbox.

```matlab
[loss, predictions] = train_xor();
assert(loss < 0.2);
```

Requires MATLAB or GNU Octave. Only statically inspected here because neither runtime is installed in the build environment.
