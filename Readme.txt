Trial class
Episode class
ModeID class
SystemID class
文件结构：
project main文件
	->ThrusterModel.py
		->若已有拟合参数文件，则读参数文件
		->若无，读csv文件实验数据
		->showfigure(), 画csv文件中的实验数据
		->fitting实验数据，得到propulsion function, 写入参数文件
		->thruster data file

	->Sim
		->读csv文件名，确定PWM command
		->USVmodel.py
			->
			->根据预设参数，更新USV状态
			->OASES class, 仿真path
			->画出路径
				
	->Exp
		->读csv文件
		->画csv文件中的实验数据 path
		->根据sim返回的path求error
		->保存error最小的一组参数和error
		->画图

	->common functions

	-> Configurations
		->USV_extension_0.csv
			->m1 
			......
		->Thruster1.csv
