Se esse códgo foi útil para você, por gentileza, dê os devidos crédtios. 

Abaixo segue algumas informações importantes:
1 - o termo "cd" é o fator de acoplamento. Você pode variar esse valor, caso queira. A depender do valor utilizado, os dois osciladores sincronizarão ou não.
2 - o termo "kp" corresponde a matrix de acoplamento. Essa matriz é responsável por determinar qual variável de estado (V1 ou V2 ou I) será utilizada no acoplamento. Se kp = [1,0,0], significa que você deseja acoplar via a variável V1; se kp = [0,1,0], a variável V2 será utilizada no acoplamento; e se kp = [0,0,1], neste, será a variável I. Lembre-se de que em kp deve-se utilizar somente 1 ou 0. 
3 - se cd = 0 e kp = [0,0,0], significa que os osciladores não irão acoplar.
