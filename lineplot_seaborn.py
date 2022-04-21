import matplotlib.pyplot as plt, seaborn as sns
import pandas as pd



results_file="results.csv"
results=pd.read_csv(results_file, encoding='utf-8')

centralized_results=results[results["Centralized"]=="Centralized"]
federated_results=results[results["Centralized"]=="Federated"]
centralized_results=centralized_results.rename(columns={"Accuracy":"Centralized Accuracy","Loss":"Centralized Loss"})
federated_results=federated_results.rename(columns={"Accuracy":"Federated Accuracy","Loss":"Federated Loss"})

#Get average grouped by "Number of Clients"
centralized_results=centralized_results.groupby(['Number of Clients'],).mean()
federated_results=federated_results.groupby(['Number of Clients'],).mean()

summarized_results=pd.merge(centralized_results,federated_results,on='Number of Clients')


accuracy_plot_data=summarized_results[["Federated Accuracy","Centralized Accuracy"]]

accuracy_plot=sns.lineplot(data=accuracy_plot_data)
plt.savefig("accuracy plot seaborn.png", bbox_inches="tight")
plt.clf()




loss_plot_data=summarized_results[["Federated Loss","Centralized Loss"]]

loss_plot=sns.lineplot(data=loss_plot_data)
plt.savefig("loss plot seaborn.png", bbox_inches="tight")
plt.clf()

#print(centralized_results)
#print(federated_results)

#summarized_results=results.groupby(['Number of Clients',"Centralized"]).mean()
#print(summarized_results)

#accuracy_plot_data = summarized_results.pivot('Number of Clients',"Centralized", "Accuracy")
#print(accuracy_plot_data)

#accuracy_plot=sns.lineplot(data=accuracy_plot_data)
#plt.savefig("accuracy plot seaborn.png", bbox_inches="tight")

#accuracy_plot=sns.lineplot(data=[centralized_results["Accuracy"],federated_results["Accuracy"]])
#accuracy_plot.set_xticklabels(accuracy_plot.get_xticklabels(), rotation=90)
#plt.legend([],[], frameon=False)
#plt.savefig("accuracy plot seaborn.png", bbox_inches="tight")
#plt.clf()

#specified_colour_count=colour_count[specified_colours]
#grafico=sns.barplot(specified_colour_count.index.tolist(), specified_colour_count.values.tolist(),hue=specified_colour_count.index.tolist(), palette=colour_dictionary,dodge = False,linewidth=1,edgecolor=".2")
#plt.legend([],[], frameon=False) 
#if label=="name":
#grafico.set_xticklabels(grafico.get_xticklabels(), rotation=90)
#plt.savefig(output_file+" "+label+".png", bbox_inches="tight")