
void mxm(int aD1,int aD2,double a[aD1][aD2],int bD1,int bD2,double b[bD1][bD2],int cD1,int cD2,double c[cD1][cD2]){

	int i;
	int j;
	int k;

	for(i = 0; i < cD1; i++){
		for(j = 0; j < cD2; j++){
			for(k = 0; k < aD2; k++){
				c[i][j] += a[i][k] * b[k][j];
			}
		}
	}

}