#define nelt 100
#define lz 10
#define lx 10
#define ly 10

void local_grad3(double u1[nelt][lx*ly][lz],double Dt[lx][ly],double u[nelt][lx][ly][lx],double D[lx][ly],double u2[nelt][lx][ly*lz],int ly*lz,double ut[nelt][lx][ly*lz],double us[nelt][lx][ly][lx],int lx*ly,double ur[nelt][lx*ly][lz]){

	int e;
	int j;
	int i;
	int k;
	int m;

	for(e = 0; e < nelt; e++){
		for(j = 0; j < lx*ly; j++){
			for(i = 0; i < lz; i++){
				for(k = 0; k < lx; k++){
					ur[e][j][i] += D[k][i]*u1[e][j][k];
				}
			}
		}
	}

	for(e = 0; e < nelt; e++){
		for(j = 0; j < lx; j++){
			for(i = 0; i < ly; i++){
				for(k = 0; k < lx; k++){
					for(m = 0; m < ly; m++){
						us[e][j][i][k] += u[e][j][m][k]*Dt[i][m];
					}
				}
			}
		}
	}

	for(e = 0; e < nelt; e++){
		for(j = 0; j < lx; j++){
			for(i = 0; i < ly*lz; i++){
				for(k = 0; k < lx; k++){
					ut[e][j][i] += u2[e][k][i]*Dt[j][k];
				}
			}
		}
	}

}