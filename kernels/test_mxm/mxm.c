void mxm(double *A,double *B,double *C)
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
   param TX0[] = ['j','i'];
   param TY0[] = ['1'];
   param BX0[] = ['i','j'];
   param BY0[] = ['1'];


   param UF_0[] = [1,2,3,4,5,6,7,8,9,10];

   constraint L01 = ((TX0 == 'j' and TY0 != 'j' and BX0 != 'j' and BY0 != 'j')) or 
 		    ((TX0 == 'i' and TY0 != 'i' and BX0 != 'i' and BY0 != 'i'));


   constraint L03 = ((TX0 != 'i' and TY0 != 'i' and BX0 == 'i' and BY0 != 'i')) or 
 		    ((TX0 != 'j' and TY0 != 'j' and BX0 == 'j' and BY0 != 'j'));



 }
 def input_params {
   param N[] = [10];
   param M[] = [10];
 }
  def input_vars {
   decl dynamic double A[N*M] = random;
   decl dynamic double B[N*M] = random;
   decl dynamic double C[M*N] = random;
}
 def search {
   arg algorithm = 'Exhaustive';
   
 }
   ) @*/
/*@ begin CHiLL ( 


	cuda(0,block={BX0},thread={TX0})

	registers(0,"k")
	unroll(0,"k",UF_0)
   ) @*/

  int i,k,j,dummyLoop;
  for (dummyLoop=0; dummyLoop<1; dummyLoop++){

  for (i=0; i<M; i++){
   for (j=0; j<N; j++){
    for (k=0; k<M; k++){

     C[i*N + j ] = C[i*N + j ] + (A[i*M + k ] * B[k*M + j ]);

    }
   }
  }

  } //end of dummy 
/*@ end @*/   // CHiLL

/*@ end @*/   // PerfTuning

}
