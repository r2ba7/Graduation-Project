/*
 * main.c
 *
 *  Created on: Mar 23, 2022
 *      Author: Hesha
 */


#include "STD_TYPES.h"
#include "BIT_MATHS.h"
#include "GPIO_Int.h"


int main()
{
	/****************************************************************/
	//set pin0 in port b as output pin
	GPIO_VoidEnablePort(PORT_B);
	GPIO_VoidSetPinDir(PORT_B,PIN_0,OUTPUT_PIN);
	// set
	GPIO_VoidSetPinValue(PORT_B,PIN_0,HIGH);
	// clear
	GPIO_VoidSetPinValue(PORT_B,PIN_0,LOW);
	/****************************************************************/
	//set pin2 in port F as input pin with pull up
	GPIO_VoidEnablePort(PORT_F);
	GPIO_VoidSetPinDir(PORT_F,PIN_2,INPUT_PIN);
	GPIO_VoidSetPinPullUp(PORT_F,PIN_2);
	// read
	u8 x = GPIO_U8GetPinValue(PORT_F,PIN_2);
	/***************************************************************/
	while (1)
	{
		***********
		**********
		*********************
		*******
	}
}
