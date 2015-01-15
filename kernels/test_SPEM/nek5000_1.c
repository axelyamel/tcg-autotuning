void nek5000(double *A,double *C,double *temp3,double *B,double *U,double *D)
{
/*@ begin PerfTuning ( 
def build {
   arg build_command = 'g++ -O3';
   arg libs = 'rose__orio_chill_.o -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -lcudart -lcuda -lm -lrt';
 }
 def performance_counter {
   arg repetitions = 100;
 }
 def performance_params {
   param TX0[] = ['k','j','n'];
   param TY0[] = ['1','k','j','n'];
   param BX0[] = ['k','j','n'];
   param BY0[] = ['1','k','j','n'];
   param TX1[] = ['k','n'];
   param TY1[] = ['1','k','j','n'];
   param BX1[] = ['k','j','n'];
   param BY1[] = ['1','k','j','n'];


   param UF_0[] = [1,2,3,4,5,6,7,8,9,10];
   param UF_1[] = [1,2,3,4,5,6,7,8,9,10];

   constraint L01 = ((TX0 == 'k' and TY0 != 'k' and BX0 != 'k' and BY0 != 'k')) or 
 		    ((TX0 == 'j' and TY0 != 'j' and BX0 != 'j' and BY0 != 'j')) or 
 		    ((TX0 == 'n' and TY0 != 'n' and BX0 != 'n' and BY0 != 'n'));

   constraint L02 = ((TX0 != '1' and TY0 == '1' and BX0 != '1' and BY0 != '1')) or 
 		    ((TX0 != 'k' and TY0 == 'k' and BX0 != 'k' and BY0 != 'k')) or 
 		    ((TX0 != 'j' and TY0 == 'j' and BX0 != 'j' and BY0 != 'j')) or 
 		    ((TX0 != 'n' and TY0 == 'n' and BX0 != 'n' and BY0 != 'n'));

   constraint L03 = ((TX0 != 'k' and TY0 != 'k' and BX0 == 'k' and BY0 != 'k')) or 
 		    ((TX0 != 'j' and TY0 != 'j' and BX0 == 'j' and BY0 != 'j')) or 
 		    ((TX0 != 'n' and TY0 != 'n' and BX0 == 'n' and BY0 != 'n'));

   constraint L04 = ((TX0 != '1' and TY0 != '1' and BX0 != '1' and BY0 == '1')) or 
 		    ((TX0 != 'k' and TY0 != 'k' and BX0 != 'k' and BY0 == 'k')) or 
 		    ((TX0 != 'j' and TY0 != 'j' and BX0 != 'j' and BY0 == 'j')) or 
 		    ((TX0 != 'n' and TY0 != 'n' and BX0 != 'n' and BY0 == 'n'));

   constraint L11 = ((TX1 == 'k' and TY1 != 'k' and BX1 != 'k' and BY1 != 'k')) or 
 		    ((TX1 == 'n' and TY1 != 'n' and BX1 != 'n' and BY1 != 'n'));

   constraint L12 = ((TX1 != '1' and TY1 == '1' and BX1 != '1' and BY1 != '1')) or 
 		    ((TX1 != 'k' and TY1 == 'k' and BX1 != 'k' and BY1 != 'k')) or 
 		    ((TX1 != 'j' and TY1 == 'j' and BX1 != 'j' and BY1 != 'j')) or 
 		    ((TX1 != 'n' and TY1 == 'n' and BX1 != 'n' and BY1 != 'n'));

   constraint L13 = ((TX1 != 'k' and TY1 != 'k' and BX1 == 'k' and BY1 != 'k')) or 
 		    ((TX1 != 'j' and TY1 != 'j' and BX1 == 'j' and BY1 != 'j')) or 
 		    ((TX1 != 'n' and TY1 != 'n' and BX1 == 'n' and BY1 != 'n'));

   constraint L14 = ((TX1 != '1' and TY1 != '1' and BX1 != '1' and BY1 == '1')) or 
 		    ((TX1 != 'k' and TY1 != 'k' and BX1 != 'k' and BY1 == 'k')) or 
 		    ((TX1 != 'j' and TY1 != 'j' and BX1 != 'j' and BY1 == 'j')) or 
 		    ((TX1 != 'n' and TY1 != 'n' and BX1 != 'n' and BY1 == 'n'));


 }
 def input_params {
   param N[] = [10];
   param J[] = [10];
   param M[] = [10];
   param I[] = [10];
   param L[] = [10];
   param K[] = [10];
 }
  def input_vars {
   decl dynamic double A[L*K] = random;
   decl dynamic double C[N*I] = random;
   decl dynamic double temp3[N*J*K] = random;
   decl dynamic double B[M*J] = random;
   decl dynamic double U[L*M*N] = random;
   decl dynamic double D[I*J*K] = random;
}
 def search {
   arg algorithm = 'Exhaustive';
 }
   ) @*/
/*@ begin CHiLL ( 

	distribute(1)

	cuda(0,block={BX0,BY0},thread={TX0,TY0})
	cuda(1,block={BX1,BY1},thread={TX1,TY1})

	registers(0,"l")
	registers(1,"l")
	unroll(0,"m",UF_0)
	unroll(1,"l",UF_1)
   ) @*/

  int l,k,m,j,n,dummyLoop;
  for (dummyLoop=0; dummyLoop<1; dummyLoop++){

  for (n=0; n<N; n++){
   for (j=0; j<J; j++){
    for (k=0; k<K; k++){
     for (l=0; l<L; l++){
      for (m=0; m<M; m++){

       temp3[n*J*K + j*K + k ] = temp3[n*J*K + j*K + k ] + (A[l*K + k ] * B[m*J + j ] * U[l*M*N + m*N + n ]);

      }
     }
    }
   }
  }

  for (n=0; n<I; n++){
   for (j=0; j<J; j++){
    for (k=0; k<K; k++){
     for (l=0; l<N; l++){

      D[n*J*K + j*K + k ] = D[n*J*K + j*K + k ] + (C[l*I + n ] * temp3[l*J*K + j*K + k ]);

     }
    }
   }
  }

  } //end of dummy 
/*@ end @*/   // CHiLL

/*@ end @*/   // PerfTuning

}