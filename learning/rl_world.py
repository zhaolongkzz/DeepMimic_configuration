import numpy as np
import learning.agent_builder as AgentBuilder
import learning.tf_util as TFUtil
from learning.rl_agent import RLAgent
from util.logger import Logger


class RLWorld(object):
    def __init__(self, env, arg_parser):
        # shield gpu using
        # os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
        TFUtil.disable_gpu()

        # read all the arguments in the world
        self.env = env
        self.arg_parser = arg_parser
        self._enable_training = True
        self.train_agents = []
        self.parse_args(arg_parser)

        # set agent, model and so on, and read the arguments in args.txt
        self.build_agents()

        return

    def get_enable_training(self):
        return self._enable_training

    def set_enable_training(self, enable):
        self._enable_training = enable
        for i in range(len(self.agents)):
            curr_agent = self.agents[i]
            if curr_agent is not None:
                enable_curr_train = self.train_agents[i] if (len(self.train_agents) > 0) else True
                curr_agent.enable_training = self.enable_training and enable_curr_train

        if (self._enable_training):
            self.env.set_mode(RLAgent.Mode.TRAIN)
        else:
            self.env.set_mode(RLAgent.Mode.TEST)

        return

    enable_training = property(get_enable_training, set_enable_training)

    def parse_args(self, arg_parser):
        self.train_agents = self.arg_parser.parse_bools('train_agents')
        num_agents = self.env.get_num_agents()
        assert(len(self.train_agents) == num_agents or len(self.train_agents) == 0)

        return

    def shutdown(self):
        self.env.shutdown()
        return

    def build_agents(self):
        # deepmimic_env.get_num_agents(): self._core.GetNumAgents()
        num_agents = self.env.get_num_agents()      # if num_agents is 2 or more, we can use multi-agents
        self.agents = []

        Logger.print('')
        Logger.print('Num Agents: {:d}'.format(num_agents))

        # recognize 'agent_files'
        agent_files = self.arg_parser.parse_strings('agent_files')
        assert(len(agent_files) == num_agents or len(agent_files) == 0)

        # model_files, but it comment out
        model_files = self.arg_parser.parse_strings('model_files')
        assert(len(model_files) == num_agents or len(model_files) == 0)

        # output and intermediate output
        output_path = self.arg_parser.parse_string('output_path')
        int_output_path = self.arg_parser.parse_string('int_output_path')

        for i in range(num_agents):
            # data/agents/ct_agent_humanoid_ppo.txt to set two agents
            curr_file = agent_files[i]
            # read file and build agent, if you have more agents, it will build more class
            curr_agent = self._build_agent(i, curr_file)

            if curr_agent is not None:
                # rl_agent.output_dir
                curr_agent.output_dir = output_path
                curr_agent.int_output_dir = int_output_path
                # print current agent state (StateDim 197, GoalDim 0, ActionDim 36)
                Logger.print(str(curr_agent))

                if (len(model_files) > 0):
                    curr_model_file = model_files[i]
                    if curr_model_file != 'none':
                        curr_agent.load_model(curr_model_file)

            self.agents.append(curr_agent)
            Logger.print('')

        self.set_enable_training(self.enable_training)

        return

    def update(self, timestep):
        self._update_agents(timestep)
        self._update_env(timestep)
        return

    def reset(self):
        self._reset_agents()
        self._reset_env()
        return

    def end_episode(self):
        self._end_episode_agents()
        return

    def _update_env(self, timestep):
        self.env.update(timestep)
        return

    def _update_agents(self, timestep):
        for agent in self.agents:
            if (agent is not None):
                # rl_agent update
                agent.update(timestep)
        return

    def _reset_env(self):
        self.env.reset()
        return

    def _reset_agents(self):
        for agent in self.agents:
            if (agent != None):
                agent.reset()
        return

    def _end_episode_agents(self):
        for agent in self.agents:
            if (agent != None):
                agent.end_episode()
        return

    def _build_agent(self, id, agent_file):
        # represent the agent id and file_name
        Logger.print('Agent {:d}: {}'.format(id, agent_file))
        if (agent_file == 'none'):
            agent = None
        else:
            # build PPO Agent class => agent
            agent = AgentBuilder.build_agent(self, id, agent_file)
            assert (agent != None), 'Failed to build agent {:d} from: {}'.format(id, agent_file)

        return agent
