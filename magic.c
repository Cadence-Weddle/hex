 @staticmethod
    #Going to try to rewrite this function is Pure C and interface with Python
    #-Jonathan Z. 12/3/2017 8:47 PM EST
    def generate_graph(values):
            cell_neighbor_weights = (1, 10, 11)  # Negatives are redundant
            graphs = []
            for value in values:
                for weight in cell_neighbor_weights:
                    if 0 <= value+weight <= 120:
                        in_graphs_flag = False
                        for independent_graph in graphs:
                            if value in independent_graph:
                                if value+weight not in independent_graph:
                                    independent_graph.extend([value+weight])
                                in_graphs_flag = True
                        if in_graphs_flag is False:
                            if value+weight in values:
                                graphs.append([value, value+weight])
                            else:
                                graphs.append([value])
            return graphs


#include <>

int check(int values[])
{
	int cell_neighbor_weights[3]={1,10,11}
	""graphs = []
	for (int value_index = 0; value_index < (sizeof(values)/sizeof(values[0])); ++i)
	{
		for (int weight_index = 0; weight_index < 3; ++i)
		{
			if (0<= value+weight[weight_index]<=120)
			{
				int in_graphs_flag = 0
				for (int independent_graph_index = 0; independent_graph_index < (sizeof(graphs)/sizeof(graphs[0])); ++independent_graph_index) /* Might Not Work*/
				{
					if (/* condition */)
					{
						if (/* condition */)
						{
							/* code */
						}
				if (/* condition */)
				{
					if (/* condition */)
					{
						/* code */
					}
					else
					{

					}
				}
					}
				}
			}
		}
	}

	/* code */
	return 0;
}

