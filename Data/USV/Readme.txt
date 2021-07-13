USV上推进器分布：
	以USV的向前方向为上
	则分布为1在下，2在右，3在上，4在左
	推力方向1和3向右，2和4向上

数据文件结构：
->Extension_number
	->Circle
		->Anticlockwise
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
		->Clockwise
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
	->Spinning
		->Anticlockwise
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
		->Clockwise
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
	->StraigntLine
		->Backward
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
		->Forward
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
		->Leftward
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......
		->Rightward
			->PWM1_n_PWM2_n_PWM3_n_PWM4_n
			......


