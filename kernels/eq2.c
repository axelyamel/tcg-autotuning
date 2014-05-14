#define N 10

void local_grad3(double *A,double *B,double *u,double *w,double *C,double *w){

	int i;
	int j;
	int k;

	for(i = 0; i < N; i++){
		for(j = 0; j < N; j++){
			for(k = 0; k < N; k++){
				w[i*N + j] += u[i*N + k]*B[k*N + j];
			}
		}
	}

	for(i = 0; i < N; i++){
		for(j = 0; j < N; j++){
			for(k = 0; k < N; k++){
				C[i*N + j] += A[i*N + k]*w[k*N + j];
			}
		}
	}

}