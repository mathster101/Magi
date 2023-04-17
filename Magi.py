import Neo
import multiprocessing as mp



def new_bookkeeper(free_port):
    new_bookkeeper = mp.Process(target=bookkeeper,args = (free_port,))
    return new_bookkeeper

def bookkeeper(port):
    queue = []
    neo_inst = Neo.Neo()
    neo_inst.start_server(PORT=port)
    neo_inst.get_new_conn()
    while True:
        #neo_inst.get_new_conn()
        rcvd = neo_inst.receive_data()
        if rcvd == "get":
            if len(queue) == 0:
                data = None
            else:
                data = queue.pop()
            neo_inst.send_data(data)

        elif rcvd[0] == "put":
            queue.append(rcvd[1])
            neo_inst.send_data("done")
        
        elif rcvd == "debug":
            print(queue)
        
        elif rcvd == "kill":
            #print("terminate")
            break


class Magi():
    def __init__(self):
        self.free_port = 1234
        self.bookkeepers = []
        self.connected_to_queue = False
        self.neo = Neo.Neo()

    def __del__(self):
        try:
            self.neo.close_conn()
        except:
            pass

    def process(self,target,args):
        proc = mp.Process(target=target, args=args)
        return proc

    def queue(self):
        self.bookkeepers.append(new_bookkeeper(self.free_port))
        self.bookkeepers[-1].start()
        self.free_port += 1
        return [self.free_port - 1, self.neo.get_my_ip()] 

    def queue_put(self,q_details, data):
        if not self.connected_to_queue:
            self.neo.connect_client(PORT=q_details[0], IP=q_details[1])
            self.connected_to_queue = True
        self.neo.send_data(["put",data])
        return self.neo.receive_data()

    def queue_get(self,q_details):
        if not self.connected_to_queue:
            self.neo.connect_client(PORT=q_details[0], IP=q_details[1])
            self.connected_to_queue = True
        self.neo.send_data("get")
        return self.neo.receive_data()
    
    def kill_queues(self):
        while len(self.bookkeepers) > 0:
            p = self.bookkeepers.pop()
            p.kill()




if __name__ == "__main__":
    m = Magi()