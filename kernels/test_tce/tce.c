void c_std_d1_1(double *T2i,double *v2,double *T3)
{
/*@ begin PerfTuning ( 
def build {
   arg build_command = 'pgc++ -fast';
   arg libs = 'rose__orio_chill_.o -I/usr/local/cuda-6.5/include -L/usr/local/cuda-6.5/lib64 -lcudart -lcuda -lm -lrt';
 }def performance_counter {
   arg repetitions = 100;
 }
 def performance_params {
   param TX0[] = ["h3","h1"];
   param TY0[] = ["h3","h2","h1","p6"];
   param BX0[] = ["h3","h2","h1","p6"];
   param BY0[] = ["h3","h2","h1","p6"];


   param UF_0[] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16];
 }
 def input_params {
   param tilesize[] = [16];
 }
  def input_vars {
   decl dynamic double T2i[tilesize*tilesize*tilesize*tilesize] = random;
   decl dynamic double v2[tilesize*tilesize*tilesize*tilesize] = random;
   decl dynamic double T3[tilesize*tilesize*tilesize*tilesize*tilesize*tilesize] = random;
}
 def search {
   arg algorithm = 'Exhaustive';
 }
   ) @*/
/*@ begin CHiLL ( 


	permute(0"p5","p4",,("p6","h1","h2","h3","h7"))

	cuda(0,block={BX0,BY0},thread={TX0,TY0})

	registers(0,"h7")
	unroll(0,"h7",UF_0)
   ) @*/

  int h7,p4,p5,h1,h3,h2,p6,dummyLoop;
  for (dummyLoop=0; dummyLoop<1; dummyLoop++){

  for (h3=0; h3<tilesize; h3++){
   for (h2=0; h2<tilesize; h2++){
    for (h1=0; h1<tilesize; h1++){
     for (p6=0; p6<tilesize; p6++){
      for (p5=0; p5<tilesize; p5++){
       for (p4=0; p4<tilesize; p4++){
        for (h7=0; h7<tilesize; h7++){

         T3[h3 + tilesize*(h2 + tilesize*(h1 + tilesize*(p6 + tilesize*(p5 + tilesize*(p4)))))] = T3[h3 + tilesize*(h2 + tilesize*(h1 + tilesize*(p6 + tilesize*(p5 + tilesize*(p4)))))] - (T2i[h7 + tilesize*(p4 + tilesize*(p5 + tilesize*(h1)))] * v2[h3 + tilesize*(h2 + tilesize*(p6 + tilesize*(h7)))]);

        }
       }
      }
     }
    }
   }
  }

  } //end of dummy 
/*@ end @*/   // CHiLL

/*@ end @*/   // PerfTuning

}