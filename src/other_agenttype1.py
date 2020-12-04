from base_agent import BaseAgent


class OtherAgenttype1(BaseAgent): 

    def test(self, opponent):
        print(type(opponent) == OtherAgenttype1)
            
