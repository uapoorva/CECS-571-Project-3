#!/usr/bin/env python
# coding: utf-8

# In[2]:

from IPython import get_ipython

get_ipython().system('!pip install rdflib')


# In[16]:


import rdflib
import pandas as pd 

g = rdflib.Graph()
g.parse('data-1152.rdf')
g.parse('data-1154.rdf')
g.parse('data-1204.rdf')
g.parse('data-1205.rdf')
g.parse('data-1538.rdf')

# g.parse('Incident Response.rdf')


# In[17]:


#population by state

qres = g.query(
    """
    PREFIX fiftyone:<http://data-gov.tw.rpi.edu/vocab/p/1152/>
    PREFIX fiftyfour:<http://data-gov.tw.rpi.edu/vocab/p/1154/>

    SELECT ?state ?veteran_population_1 ?veteran_population_2
 WHERE { 
    {
        SELECT ?state (sum(xsd:decimal(?vp1152)) AS ?veteran_population_1) 
    	WHERE {
            ?s fiftyone:veteran_population ?vp1152. 
            ?s fiftyone:state ?state.
        } group by ?state order by ?state
    }
    {
        SELECT ?state_abb (sum(xsd:decimal(?vp1154)) AS ?veteran_population_2) 
    	WHERE {
            ?s fiftyfour:veteran_population ?vp1154. 
            ?s fiftyfour:state ?state1.
            bind( substr( ?state1, 1, 2 ) as ?state_abb )
        } group by ?state_abb order by ?state_abb
    }
  FILTER (?state = ?state_abb) 
} """)

result=[]
for row in qres:
    result.append([row[0],row[1],row[2]])
out=[[0 for _ in range(len(result[0]))] for _ in range(len(result)+1)]
out[0]=['State','Population Year 2007','Population Year 2008']
for i in range(len(result)):
            result[i] = list(result[i])
            for j in range(len(result[i])):
                    out[i+1][j] = str(result[i][j])
popByState = out
print(popByState)


# In[18]:


df = pd.DataFrame(out[1:], columns = ['State','Population Year 2007','Population Year 2008'])
df['Population 2007'] = df['Population Year 2007'].astype(float).astype(int).div(1000)
df['Population 2008'] = df['Population Year 2008'].astype(float).astype(int).div(1000)

df.set_index(['State'], inplace=True)
ax=df.plot.barh(figsize=(10,10))
ax.set_xlabel("Population")

ax.figure.savefig('static/vetPopulation.jpg')


# In[19]:


#
qres = g.query(
    """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX fiftytwo:<http://data-gov.tw.rpi.edu/vocab/p/1152/>
    PREFIX fiftyfour:<http://data-gov.tw.rpi.edu/vocab/p/1154/>
    SELECT ?state ?exp_year1 ?exp_year2
     WHERE { 
        {
            SELECT ?state (sum(xsd:decimal(?exp_yr1)) AS ?exp_year1) 
            WHERE {
                ?s fiftytwo:total_expenditure ?exp_yr1. 
                ?s fiftytwo:state ?state.

            } group by ?state order by ?state
        }
        {
            SELECT ?state_abb (sum(xsd:decimal(?exp_yr2)) AS ?exp_year2) 
            WHERE {
                ?s fiftyfour:total_expenditure ?exp_yr2. 
                ?s fiftyfour:state ?state1.
                bind( substr( ?state1, 1, 2 ) as ?state_abb )
            } group by ?state_abb order by ?state_abb
        }
      FILTER (?state = ?state_abb) 
    }
 """)
result=[]
for row in qres:
    result.append([row[0],row[1],row[2]])
out=[[0 for _ in range(len(result[0]))] for _ in range(len(result)+1)]
out[0]=['State','Expenditure Year 2007','Expenditure Year 2008']
for i in range(len(result)):
            result[i] = list(result[i])
            for j in range(len(result[i])):
                    out[i+1][j] = str(result[i][j])

expByState=out
print(expByState)


# In[20]:


df = pd.DataFrame(out[1:], columns = ['State','Year 2007','Year 2008'])
df['Year 2007'] = df['Year 2007'].astype(float).astype(int)
df['Year 2008'] = df['Year 2008'].astype(float).astype(int)

df.set_index(['State'], inplace=True)
ax=df.plot.bar(figsize=(10,10))
ax.set_ylabel("Expenditure")
ax.figure.savefig('static/vetExp.jpg')


# In[21]:


#veterans by age
qres = g.query(
    """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    SELECT  ?state (SUM(?age35to441) AS ?betweenageof35and44) (SUM(?age45to541) AS
  ?agebetween45and54) (SUM(?age55to641) AS ?agebetween55and64)
(SUM(?age65to741) AS ?agebetween65and74)
    WHERE {
    ?s <http://data-gov.tw.rpi.edu/vocab/p/1538/state> ?state.
    
    ?s <http://data-gov.tw.rpi.edu/vocab/p/1538/age_35_44_c_p> ?age35to44.
    BIND(IF(?age35to44 = "*", 0, xsd:integer(?age35to44)) as ?age35to441)

    ?s <http://data-gov.tw.rpi.edu/vocab/p/1538/age_45_54_c_p> ?age45to54.
        BIND(IF(?age45to54 = "*", 0, xsd:integer(?age45to54)) as ?age45to541)

    ?s <http://data-gov.tw.rpi.edu/vocab/p/1538/age_65_74_c_p> ?age65to74. 
       BIND(IF(?age65to74 = "*", 0, xsd:integer(?age65to74)) as ?age65to741)

    ?s <http://data-gov.tw.rpi.edu/vocab/p/1538/age_55_64_c_p> ?age55to64.
        BIND(IF(?age55to64 = "*", 0, xsd:integer(?age55to64)) as ?age55to641)


    } GROUP BY ?state ORDER BY ?state

 """)
result=[]
for row in qres:
    result.append([row[0],row[1],row[2],row[3],row[4]])
out=[[0 for _ in range(len(result[0]))] for _ in range(len(result)+1)]
out[0]=['State','Between age of 35 and 44','Between age of 45 and 54', 'Between age of 55 and 64', 'Between age of 65 and 74']
for i in range(len(result)):
            result[i] = list(result[i])
            for j in range(len(result[i])):
                    out[i+1][j] = str(result[i][j])
vetByAge = out
print(vetByAge)


# In[22]:


df = pd.DataFrame(out[1:], columns = ['State','Age 35 to 44','Age 45 to 54','Age 55 to 64','Age 65 to 74'])
df['Age 35 to 44'] = df['Age 35 to 44'].astype(int)
df['Age 45 to 54'] = df['Age 45 to 54'].astype(int)
df['Age 55 to 64'] = df['Age 55 to 64'].astype(int)
df['Age 65 to 74'] = df['Age 65 to 74'].astype(int)
df.set_index(['State'], inplace=True)

df.head()
ax=df.plot(kind='pie', subplots=True,
         autopct='%1.1f%%', startangle=270, fontsize=30,
         layout=(2,2), figsize=(100,100))


# In[23]:


#veterans per hospital staff (doctors and nurses) in every state
qres=g.query("""

        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix fiftyfour: <http://data-gov.tw.rpi.edu/vocab/p/1154/>
        prefix onetwofive: <http://data-gov.tw.rpi.edu/vocab/p/1202/>

        SELECT distinct ?state_abb (xsd:decimal(?veteran_population1) as ?veteran_population2 ) ((xsd:decimal(?staffNur)+ xsd:decimal(?staffPhy))  AS ?div) 
         WHERE { 
             { 
                 SELECT ?state_abb  (SUM(xsd:decimal(?veteran_population)) as ?veteran_population1)
                 WHERE { 

                         ?x fiftyfour:state ?state.
                         ?x fiftyfour:veteran_population ?veteran_population . 
                          bind( substr( ?state, 1, 2 ) as ?state_abb )

                 } 
                 group by ?state_abb 
             } 
             { 
                 SELECT ?state1 (sum(?staffing_nursing1) as ?staffNur)  (sum(?staffing_physicians1) as ?staffPhy)  
                     WHERE { 

                             ?y onetwofive:state ?state1 . 
                             ?y onetwofive:staffing_nursing ?staffing_nursing .
                             BIND(IF(?staffing_nursing = "+", 0, xsd:integer(?staffing_nursing)) as ?staffing_nursing1)
                             ?y onetwofive:staffing_physicians ?staffing_physicians.
                             BIND(IF(?staffing_physicians = "+", 0, xsd:integer(?staffing_physicians)) as ?staffing_physicians1)
                     } 
                     group by ?state1
             } 
              FILTER (?state_abb = ?state1) 
         } 
        ORDER BY ?state_abb
""")

result=[]
for row in qres:
    result.append([row[0],row[1],row[2]])
out=[[0 for _ in range(len(result[0]))] for _ in range(len(result)+1)]
out[0]=['State','Veteran Population','Staff']
for i in range(len(result)):
            result[i] = list(result[i])
            for j in range(len(result[i])):
                    out[i+1][j] = str(result[i][j])

vetForStaff = out
print(vetForStaff)


# In[24]:



df = pd.DataFrame(out[1:], columns = ['State', 'Veteran population','Staff'])
df['Veteran population'] = df['Veteran population'].astype(float).astype(int)
df['Veteran population'] = df['Veteran population'].div(1000)
df['Staff'] = df['Staff'].astype(int)
df.set_index(['State'], inplace=True)
ax=df.plot.line(figsize=(10,10))
ax.figure.savefig('static/vetStaff.jpg')


# In[25]:


#Query5: veterans population with cases
qres=g.query("""
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX fiftyfour:<http://data-gov.tw.rpi.edu/vocab/p/1154/>
    PREFIX twentytwo:<http://data-gov.tw.rpi.edu/vocab/p/1204/>
    SELECT ?state1 (xsd:decimal(?veteran_population_2) as ?veteran_population) (xsd:integer(xsd:decimal(?specialty_care_seen)+xsd:decimal(?primary_care_seen)) AS ?Total_cases)
    WHERE { 
        {
            SELECT ?state_abb (sum(xsd:decimal(?vp1154)) AS ?veteran_population_2) 
            WHERE {
                ?s fiftyfour:veteran_population ?vp1154. 
                ?s fiftyfour:state ?state.
                bind( substr( ?state, 1, 2 ) as ?state_abb )
            } group by ?state_abb order by ?state_abb
        }
       {
            SELECT ?state1 (sum(xsd:decimal(?scs30)) AS ?specialty_care_seen) (sum(xsd:decimal(?pcs30)) AS ?primary_care_seen) 
            WHERE {
                ?s1 twentytwo:specialty_care_seen_in_30_days ?scs30. 
                ?s1 twentytwo:primary_care_seen_in_30_days ?pcs30. 
                ?s1 twentytwo:state ?state1.
            } group by ?state1 order by ?state1
        }
      FILTER (?state_abb = ?state1) 
    }
""")
#print(qres)
# qres=g.query("""
#             PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#      PREFIX fiftyfour:<http://data-gov.tw.rpi.edu/vocab/p/1154/>
#      PREFIX twentytwo:<http://data-gov.tw.rpi.edu/vocab/p/1204/>
#             SELECT ?state1 (sum(xsd:decimal(?scs30)) AS ?specialty_care_seen) (sum(xsd:decimal(?pcs30)) AS ?primary_care_seen) 
#             WHERE {
#                 ?s1 twentytwo:specialty_care_seen_in_30_days ?scs30. 
#                 ?s1 twentytwo:primary_care_seen_in_30_days ?pcs30. 
#                 ?s1 twentytwo:state ?state1.
#             } group by ?state1 order by ?state1""")
result=[]
for row in qres:
    result.append([row[0],row[1],row[2]])
out=[[0 for _ in range(len(result[0]))] for _ in range(len(result)+1)]
out[0]=['State','Veteran Population','Total cases']
for i in range(len(result)):
            result[i] = list(result[i])
            for j in range(len(result[i])):
                    out[i+1][j] = str(result[i][j])

vetCases = out
print(vetCases)


# In[26]:



import pandas as pd 

df = pd.DataFrame(out[1:], columns = ['State', 'Veteran population','Total cases'])
df['Veteran population'] = df['Veteran population'].astype(float).astype(int)
df['Veteran population'] = df['Veteran population'].div(1000)
df['Total cases'] = df['Total cases'].astype(int)
df.set_index(['State'], inplace=True)

ax=df.plot.bar(figsize=(10,10),stacked=True)
ax.set_ylabel("Popluation")
ax.figure.savefig('static/vetCases.jpg')


# In[ ]:


from flask import Flask, jsonify, request, render_template, url_for
app = Flask(__name__)

@app.route('/populationByState', methods=['GET'])
def sendPopulationByState():
    return jsonify(popByState)

@app.route('/expenditureByState', methods=['GET'])
def sendExpenditureByState():
    return jsonify(expByState)

@app.route('/vetByAge', methods=['GET'])
def sendVetByAge():
    return jsonify(vetByAge)

@app.route('/vetCases', methods=['GET'])
def sendVetCases():
    return jsonify(vetCases)

@app.route('/vetPerStaff', methods=['GET'])
def sendVetPerStaff():
    return jsonify(vetForStaff)


@app.route('/fetch')
def fetch():
    return render_template('test.html')
if __name__ == "__main__":
    app.run()


# In[ ]:




