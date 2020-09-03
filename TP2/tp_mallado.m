ndim = 1;
nod_x_elem = 2; # 3; # 4; # 5;
nelementos = 4; # 5; # 6;
nnodos = (nod_x_elem-1)*nelementos+1;
L = 4.0;
H_k = 8.0;
T0 = 50.0;
T_L = 10.0;

temperatura = zeros(1, nnodos);

[coorx, conectividad, temp_fija, valor_temp_fija] = mallado(nnodos, nelementos, nod_x_elem, L, T0, T_L);

for i=1:nnodos
    if (temp_fija(i) == 1)
        temperatura(i) = valor_temp_fija(i);
    else
        temperatura(i) = (H_k/2.0)*coorx(i)*(L - coorx(i)) - ((T0 - T_L)/L)*coorx(i) + T0;
    end
end

for i=1:nelementos
    fprintf('Elemento %i: ', i);
    disp(conectividad(i,:));
end
fprintf('Temperaturas en los nodos: \n');
disp(temperatura);

figure
plot(coorx(:), temperatura)
