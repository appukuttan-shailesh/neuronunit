'''
Neuron simulator export for:

Components:
    RS (Type: izhikevich2007Cell:  v0=-0.06 (SI voltage) k=7.0E-7 (SI conductance_per_voltage) vr=-0.06 (SI voltage) vt=-0.04 (SI voltage) vpeak=0.035 (SI voltage) a=30.0 (SI per_time) b=-2.0E-9 (SI conductance) c=-0.05 (SI voltage) d=1.0E-10 (SI current) C=1.0E-10 (SI capacitance))
    RS_Iext (Type: pulseGenerator:  delay=0.5 (SI time) duration=1.0 (SI time) amplitude=1.0E-10 (SI current))
    net1 (Type: network)
    sim1 (Type: Simulation:  length=1.6 (SI time) step=2.5E-6 (SI time))


    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.5.0
         org.neuroml.model   v1.5.0
         jLEMS               v0.9.8.7

'''

import neuron

import time
h = neuron.h
h.load_file("nrngui.hoc")

h("objref p")
h("p = new PythonObject()")

class NeuronSimulation():

    def __init__(self, tstop, dt):



        # Adding simulation Component(id=sim1 type=Simulation) of network/component: net1 (Type: network)


        h(" {n_RS_pop = 1} ")
        '''
        Population RS_pop contains instances of Component(id=RS type=izhikevich2007Cell)
        whose dynamics will be implemented as a mechanism (RS) in a mod file
        '''
        h(" create RS_pop[1]")
        h(" objectvar m_RS_RS_pop[1] ")

        for i in range(int(h.n_RS_pop)):
            h.RS_pop[i].L = 10.0
            h.RS_pop[i](0.5).diam = 10.0
            h.RS_pop[i](0.5).cm = 31.830988618379067
            h.RS_pop[i].push()
            h(" RS_pop[%i]  { m_RS_RS_pop[%i] = new RS(0.5) } "%(i,i))

            h.m_RS_RS_pop[i].v0 = -60.0
            h.m_RS_RS_pop[i].k = 7.0E-4
            h.m_RS_RS_pop[i].vr = -60.0
            h.m_RS_RS_pop[i].vt = -40.0
            h.m_RS_RS_pop[i].vpeak = 35.0
            h.m_RS_RS_pop[i].a = 0.030000001
            h.m_RS_RS_pop[i].b = -0.0019999999
            h.m_RS_RS_pop[i].c = -50.0
            h.m_RS_RS_pop[i].d = 0.1
            h.m_RS_RS_pop[i].C = 1.00000005E-4           
            h.pop_section()

        # Adding input: Component(id=null type=explicitInput)

        h("objref explicitInput_RS_IextRS_pop0")
        h("RS_pop[0] { explicitInput_RS_IextRS_pop0 = new RS_Iext(0.500000) } ")

        trec = h.Vector()
        trec.record(h._ref_t)

        h.tstop = tstop

        h.dt = dt

        h.steps_per_ms = 1/h.dt

        # Display: self.display_d1
        self.display_d1 = h.Graph(0)
        self.display_d1.size(0,h.tstop,-80.0,50.0)
        self.display_d1.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
        h.graphList[0].append(self.display_d1)
        # Line, plotting: RS_pop[0]/v
        self.display_d1.addexpr("RS_pop[0].v(0.5)", "RS_pop[0].v(0.5)", 1, 1, 0.8, 0.9, 2)

        # Display: self.display_d2
        self.display_d2 = h.Graph(0)
        self.display_d2.size(0,h.tstop,-80.0,50.0)
        self.display_d2.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
        h.graphList[0].append(self.display_d2)
        # Line, plotting: RS_pop[0]/u
        self.display_d2.addexpr("m_RS_RS_pop[0].u", "m_RS_RS_pop[0].u", 1, 1, 0.8, 0.9, 2)



        # File to save: time
        # Column: time
        h(' objectvar v_time ')
        h(' { v_time = new Vector() } ')
        h(' { v_time.record(&t) } ')
        h.v_time.resize((h.tstop * h.steps_per_ms) + 1)

        # File to save: of0
        # Column: RS_pop[0]/v
        h(' objectvar v_v_of0 ')
        h(' { v_v_of0 = new Vector() } ')
        h(' { v_v_of0.record(&RS_pop[0].v(0.5)) } ')
        h.v_v_of0.resize((h.tstop * h.steps_per_ms) + 1)
        # Column: RS_pop[0]/u
        h(' objectvar v_u_of0 ')
        h(' { v_u_of0 = new Vector() } ')
        h(' { v_u_of0.record(&m_RS_RS_pop[0].u) } ')
        h.v_u_of0.resize((h.tstop * h.steps_per_ms) + 1)

        self.initialized = False

        self.sim_end = -1 # will be overwritten

        h.nrncontrolmenu()


    def run(self):

        self.initialized = True
        sim_start = time.time()


        h.run()

        self.sim_end = time.time()
        sim_time = self.sim_end - sim_start


        self.save_results()


    def advance(self):

        if not self.initialized:
            h.finitialize()
            self.initialized = True

        h.fadvance()


    def save_results(self):


        if self.sim_end < 0: self.sim_end = time.time()


        # File to save: time
        py_v_time = [ t/1000 for t in h.v_time.to_python() ]  # Convert to Python list for speed...

        f_time_f2 = open('time.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_time_f2.write('%f'% py_v_time[i])  # Save in SI units...+ '\n')
        f_time_f2.close()
      
        # File to save: of0
        py_v_v_of0 = [ float(x  / 1000.0) for x in h.v_v_of0.to_python() ]  # Convert to Python list for speed, variable has dim: voltage
        py_v_u_of0 = [ float(x  / 1.0E9) for x in h.v_u_of0.to_python() ]  # Convert to Python list for speed, variable has dim: current

        f_of0_f2 = open('RS_One.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_of0_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v_of0[i])  + '%e\t'%(py_v_u_of0[i]) + '\n')
        f_of0_f2.close()

        save_end = time.time()
        save_time = save_end - self.sim_end



if __name__ == '__main__':

    ns = NeuronSimulation(tstop=1600, dt=0.0025)

    ns.run()


#    ns.run()
