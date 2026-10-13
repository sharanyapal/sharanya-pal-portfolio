% Pure MATLAB/Octave XOR 2->8->1 network, tanh + sigmoid and momentum SGD.
% No Deep Learning Toolbox required. Invoke: train_xor
function [loss,pred] = train_xor()
 rng(17);
 X=[0 0;0 1;1 0;1 1]; Y=[0;1;1;0];
 W1=randn(2,8)*0.3; b1=zeros(1,8); W2=randn(8,1)*0.3; b2=0;
 vW1=zeros(size(W1)); vb1=zeros(size(b1)); vW2=zeros(size(W2)); vb2=0;
 alpha=.45; momentum=.75;
 for epoch=1:8500
   H=tanh(bsxfun(@plus,X*W1,b1));P=1./(1+exp(-max(-30,min(30,H*W2+b2))));
   dZ2=(P-Y)/4; dW2=H'*dZ2; db2=sum(dZ2,1);
   dZ1=(dZ2*W2').*(1-H.^2);dW1=X'*dZ1;db1=sum(dZ1,1);
   vW2=momentum*vW2-alpha*dW2;vb2=momentum*vb2-alpha*db2;
   vW1=momentum*vW1-alpha*dW1;vb1=momentum*vb1-alpha*db1;
   W2=W2+vW2;b2=b2+vb2;W1=W1+vW1;b1=b1+vb1;
 end
 H=tanh(bsxfun(@plus,X*W1,b1));pred=1./(1+exp(-(H*W2+b2)));
 loss=-mean(Y.*log(max(pred,eps))+(1-Y).*log(max(1-pred,eps)));
 disp(table(X(:,1),X(:,2),pred,'VariableNames',{'x1','x2','predicted'}));fprintf('cross entropy %.6f\n',loss);
 if any((pred>=.5)~=Y),error('XOR learning failed');end
end
