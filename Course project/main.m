str = LoadFreq('Caulobacter_vibrioides.fa');
xx4 = CalcFreq(str,4,300);
xx3 = CalcFreq(str,3,300);
xx2 = CalcFreq(str,2,300);
xx1 = CalcFreq(str,1,300);
subplot(2,2,1)
PCAFreq(xx1);
subplot(2,2,2)
PCAFreq(xx2);
subplot(2,2,3)
PCAFreq(xx3);
subplot(2,2,4)
PCAFreq(xx4);
fragn = ClustFreq(xx3,7);