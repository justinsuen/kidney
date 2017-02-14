package de.normalisiert.utils.graphs;

import java.io.*;
import java.util.List;
import java.util.HashSet;

/**
 * Reader file for elementary cycle search.
 *
 * @author Eugene Lo
 *
 */
public class Reader {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		final long startTime = System.currentTimeMillis();
		String inDir = "phase1-processed/";
		String outDir = "phase1-cycles/";
		int instance = 0;
		List cycles = null;
		try {
			///////////////////////
			// Read in todo list //
			///////////////////////
			FileReader instanceReader = new FileReader("todo.txt");
			BufferedReader bufferedInstanceReader = new BufferedReader(instanceReader);
			String instanceReaderLine = null;
			while ((instanceReaderLine = bufferedInstanceReader.readLine()) != null){
				try{
					instance = Integer.parseInt(instanceReaderLine);

					/////////////////////////////////
					// Run cycle finding algorithm //
					/////////////////////////////////
					String inFileName = inDir + instance + ".in";
					String outFileName = outDir + instance + ".in";
					String line = null;
					String children = null;

		            // FileReader reads text files in the default encoding.
		            FileReader fileReader = new FileReader(inFileName);

		            // Always wrap FileReader in BufferedReader.
		            BufferedReader bufferedReader = new BufferedReader(fileReader);
		            line = bufferedReader.readLine();
		            int dim = Integer.parseInt(line);
		            children = bufferedReader.readLine();

		            String nodes[] = new String[dim];
		            for (int i = 0; i < dim; i++) {
				 		nodes[i] = Integer.toString(i);
					}

					boolean adjMatrix[][] = new boolean[dim][dim];
					int k = 0;
		            while(((line = bufferedReader.readLine()) != null) && (k < dim)) {
		                String[] entries = line.split(" ");
		                for (int j = 0; j < dim; j++){
		                	int currInt = Integer.parseInt(entries[j]);
		                	adjMatrix[k][j] = (currInt == 1);
		                }
		                k++;
		            }   

			        FileWriter fileWriter = new FileWriter(outFileName);
			        BufferedWriter bufferedWriter = new BufferedWriter(fileWriter);

					ElementaryCyclesSearch ecs = new ElementaryCyclesSearch(adjMatrix, nodes);
					cycles = ecs.getElementaryCycles();
					if (cycles != null) {
						System.out.println("Instance: " + instance + ". " + "NumCycles: " + cycles.size());
						for (int i = 0; i < cycles.size(); i++) {
							List cycle = (List) cycles.get(i);
							if (cycle.size() > 5) continue;
							for (int j = 0; j < cycle.size(); j++) {
								String node = (String) cycle.get(j);
								if (j < cycle.size() - 1) {
									bufferedWriter.write(node + " -> ");
								} else {
									bufferedWriter.write(node);
								}
							}
							bufferedWriter.newLine();
						}
					} else {
						System.out.println("Instance " + instance + " failed.");
						continue;
					}

			            // Always close files.
			            bufferedReader.close();
			            bufferedWriter.close();
			        }
			        catch(InterruptedException ex) {
			        	System.out.println("Instance " + instance + " failed.");
			        	// if (cycles != null) System.out.println(cycles.size());
			        	continue;
			        }
			    }
		    bufferedInstanceReader.close();
		}
    
        catch(FileNotFoundException ex) {
            System.out.println(
                "Unable to open file");
        }
        catch(IOException ex) {
            ex.printStackTrace();
        }
        catch(NumberFormatException ex) {
        	ex.printStackTrace();
        }


        final long endTime = System.currentTimeMillis();
		System.out.println("Total execution time: " + (endTime - startTime) * 1000 + "s");
	}
}
