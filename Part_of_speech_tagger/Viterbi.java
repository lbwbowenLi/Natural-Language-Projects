
import java.util.*;
public class Viterbi {
	public static int[] max(double[][] s,int b){
		int[] a=new int[b];
		for(int i=0;i<b;i++){
			double mx=0;
			for(int j=1;j<=4;j++){
				if(s[i][j]>mx){
					mx=s[i][j];
					a[i]=j;
				}
					
			}
		}
		return a;
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		In in=new In("sents.txt");
		String[] sents=new String[100];
		int size=0;
		while(in.hasNextLine()){
			sents[size]=in.readLine().toLowerCase();
			size+=1;
		}
		String[][] sentss=new String[size][100];
		for(int i=0;i<size;i++){
			sentss[i]=sents[i].split(" ");
		}
		HashMap mp=new HashMap();
		double[][] ps=new double[6][6];
		mp.put("phi",0);
		mp.put("noun",1);
		mp.put("verb",2);
		mp.put("inf",3);	
		mp.put("prep",4);
		mp.put("fin",5);
		In inp=new In("probs.txt");
		String[] probs=new String[100];
		int sizep=0;
		while(inp.hasNextLine()){
			probs[sizep]=inp.readLine().toLowerCase();
			sizep+=1;
		}
		String[][] probss=new String[sizep][3];
		for(int i=0;i<sizep;i++){
			probss[i]=probs[i].split(" ");
		}
		int x;
		double b;
		for(int i=0;i<sizep;i++){
				probss[i][2]=probss[i][2].substring(1);
				b=Double.parseDouble(probss[i][2])/100;
				 if(mp.containsKey(probss[i][0]))
					 if(mp.containsKey(probss[i][1])){
						 ps[(int)mp.get(probss[i][0])][(int)mp.get(probss[i][1])]=b;
						// System.out.println(ps[(int)mp.get(probss[i][0])][(int)mp.get(probss[i][1])]);
					 }
				 		 //System.out.println(x);
		}
		for(int i=0;i<6;i++)
			for(int j=0;j<6;j++)
				if(ps[i][j]==0)
					ps[i][j]=0.0001;
		HashMap mpwords=new HashMap();
		double[][] wordsp=new double[100][5];
		int k=0;
		for(int i=0;i<sizep;i++){
			if(mp.containsKey(probss[i][0])==false){
				if(mpwords.containsKey(probss[i][0])==false){
					mpwords.put(probss[i][0], k);
					wordsp[k][(int)mp.get(probss[i][1])]=Double.parseDouble(probss[i][2])/100;
					//System.out.println(wordsp[k][(int)mp.get(probss[i][1])]);
					k++;
				}
				else{
					wordsp[(int)mpwords.get(probss[i][0])][(int)mp.get(probss[i][1])]=Double.parseDouble(probss[i][2])/100;
					//System.out.println(wordsp[(int)mpwords.get(probss[i][0])][(int)mp.get(probss[i][1])]);
				}
			}
		}
		for(int i=0;i<k;i++){
			for(int j=0;j<5;j++)
				if(wordsp[i][j]==0)
					wordsp[i][j]=0.0001;
		}
		//System.out.println(sentss[2][1]);
/////////////////////////////////vierbi start	   
		for(int i=0;i<size;i++){
			System.out.println("PROCESSING SENTENCE: "+sents[i]);
			System.out.print("\n");
			System.out.println("FINAL VITERBI NETWORK");
			//System.out.print("\n");
			double[][] vb=new double[sentss[i].length+1][6];
			int[][] back=new int[sentss[i].length+1][6];
			//double[] vbf=new double[sentss [i].length+1];		
			for(int j=1;j<5;j++)
				vb[0][j]=1;
			//double tmp=0;
			for(int vbk=1;vbk<=sentss[i].length;vbk++){
				if(vbk==1){
					for(int v=1;v<=4;v++){
						if(mpwords.containsKey(sentss[i][vbk-1]))
						vb[1][v]=1*ps[v][0]*wordsp[(int)mpwords.get(sentss[i][vbk-1])][v];
						else
						vb[1][v]=1*ps[v][0]*0.0001;
						//System.out.print(vb[1][v]+" ");
					}
					//System.out.print("\n");
				}
				else{
					for(int v=1;v<=4;v++){
						vb[vbk][v]=0;
						double tmp=0;
						for(int w=1;w<=4;w++){
							//System.out.println(mpwords.get(sentss[i][vbk-1]));
							if(mpwords.containsKey(sentss[i][vbk-1]))
							 tmp=vb[vbk-1][w]*ps[v][w]*wordsp[(int)mpwords.get(sentss[i][vbk-1])][v];
							else
							 tmp=vb[vbk-1][w]*ps[v][w]*0.0001;

							 //System.out.println(tmp);
							if(tmp>=vb[vbk][v]){
								vb[vbk][v]=tmp;
								back[vbk][v]=w;
							}
						}
						//System.out.print(vb[vbk][v]+" ");
					}
					//System.out.print("\n");
				}
			}
///////////////////////////////print part1
			String[] ss={"noun","verb","inf","prep"};
			for(int pr=1;pr<=sentss[i].length;pr++){
				System.out.println("P("+sentss[i][pr-1]+"=noun"+")="+String.format("%.11f",vb[pr][1]));
				System.out.println("P("+sentss[i][pr-1]+"=verb"+")="+String.format("%.11f",vb[pr][2]));
				System.out.println("P("+sentss[i][pr-1]+"=inf"+")="+String.format("%.11f",vb[pr][3]));
				System.out.println("P("+sentss[i][pr-1]+"=prep"+")="+String.format("%.11f",vb[pr][4]));
			}
			System.out.print("\n");
			System.out.println("FINAL BACKPTR NETWORK");
			for(int pr=2;pr<=sentss[i].length;pr++){
				System.out.println("Backptr("+sentss[i][pr-1]+"=noun"+")="+ss[back[pr][1]-1]);
				System.out.println("Backptr("+sentss[i][pr-1]+"=verb"+")="+ss[back[pr][2]-1]);
				System.out.println("Backptr("+sentss[i][pr-1]+"=inf"+")="+ss[back[pr][3]-1]);
				System.out.println("Backptr("+sentss[i][pr-1]+"=prep"+")="+ss[back[pr][4]-1]);
			}
			System.out.print("\n");
			double maxv=0;
			for(int vbi=1;vbi<=4;vbi++){
				double tp2=vb[sentss[i].length][vbi]*ps[5][vbi];
				if(tp2>maxv)
					maxv=tp2;
			}
			System.out.println("BEST TAG SEQUENCE HAS PROBABILITY = "+String.format("%.11f",maxv));
			
			
			for(int mi=1;mi<=sentss[i].length;mi++){		
				double m=0;
				int n=0;
				for(int cur=1;cur<=4;cur++){
					if(vb[mi][cur]>m){
						m=vb[mi][cur];
						n=cur;   
					}
				}
				//System.out.println(n);
				System.out.println(sentss[i][mi-1]+"->"+ss[n-1]);
			}
///////////////////////////forward
			System.out.print("\n");
			System.out.println("FORWARD ALGORITHM RESULTS");
			System.out.print("\n");
			double[][] vb2=new double[sentss[i].length+1][6];
			//double[] vbf=new double[sentss[i].length+1];		
			for(int j=1;j<5;j++)
				vb2[0][j]=1;
			
			for(int vbk=1;vbk<=sentss[i].length;vbk++){
				if(vbk==1){
					for(int v=1;v<=4;v++){
						if(mpwords.containsKey(sentss[i][vbk-1]))
						vb2[1][v]=1*ps[v][0]*wordsp[(int)mpwords.get(sentss[i][vbk-1])][v];
						else
						vb2[1][v]=1*ps[v][0]*0.0001;
						//System.out.print(vb[1][v]+" ");
					}
					//System.out.print("\n");
				}
				else{
					for(int v=1;v<=4;v++){
						vb2[vbk][v]=0;
						double tmp2=0;
						for(int w=1;w<=4;w++){
							//System.out.println(mpwords.get(sentss[i][vbk-1]));
							if(mpwords.containsKey(sentss[i][vbk-1]))
							 tmp2+=vb2[vbk-1][w]*ps[v][w]*wordsp[(int)mpwords.get(sentss[i][vbk-1])][v];
							else
							 tmp2+=vb2[vbk-1][w]*ps[v][w]*0.0001;

							 //System.out.println(tmp);
							//if(tmp2>=vb2[vbk][v])
								vb2[vbk][v]=tmp2;
						}
						//System.out.print(vb[vbk][v]+" ");
					}
					//System.out.print("\n");
				}
			}
			for(int pr=1;pr<=sentss[i].length;pr++){
				System.out.println("P("+sentss[i][pr-1]+"=noun"+")="+String.format("%.11f",vb2[pr][1]));
				System.out.println("P("+sentss[i][pr-1]+"=verb"+")="+String.format("%.11f",vb2[pr][2]));
				System.out.println("P("+sentss[i][pr-1]+"=inf"+")="+String.format("%.11f",vb2[pr][3]));
				System.out.println("P("+sentss[i][pr-1]+"=prep"+")="+String.format("%.11f",vb2[pr][4]));
			}
			System.out.print("\n");
////////////////////////////
		}
	}

}
