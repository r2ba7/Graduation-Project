/***************************************************************/
/*  Author 	     : Hashim Sobhi                               **/
/*  Date    	 : 23.3.2022                                  **/
/*  Description  : GPIO driver 	                	          **/
/*  Version 	 : 1.0                                        **/
/***************************************************************/
#include "STD_TYPES.h"
#include "BIT_MATHS.h"
#include "GPIO_Int.h"
#include "GPIO_Reg.h"
void Delay(u32 counter);
void Delay(u32 counter)
{
	u32 i = 0;
	for(i = 0; i<counter; i++);	
}

void GPIO_VoidEnablePort(u8 copy_u8PORT)
{
	switch(copy_u8PORT)
	{
		case PORT_A: 
		SET_BIT(RCGCGPIO,PIN_0); // enable clock 
		Delay(2); //waste time to make system stable
		GPIO_PORTA_LOCK_R = 0x4C4F434B;  // unlock CR 
		GPIO_PORTA_CR_R |= 0xFF; // allow changes all pins
		GPIO_PORTA_AFSEL_R |= 0x00; //disable alternative functions all pins
		GPIO_PORTA_DEN_R |= 0xFF; //set digital port 
		break;
		
		case PORT_B: 
		SET_BIT(RCGCGPIO,PIN_1); // enable clock 
		Delay(2); //waste time to make system stable
		GPIO_PORTB_LOCK_R = 0x4C4F434B;  // unlock CR 
		GPIO_PORTB_CR_R |= 0xFF; // allow changes all pins
		GPIO_PORTB_AFSEL_R |= 0x00; //disable alternative functions all pins
		GPIO_PORTB_DEN_R |= 0xFF; //set digital port 
		break;
		
		case PORT_C: 
		SET_BIT(RCGCGPIO,PIN_2); // enable clock 
		Delay(2); //waste time to make system stable
		GPIO_PORTC_LOCK_R = 0x4C4F434B;  // unlock CR 
		GPIO_PORTC_CR_R |= 0xFF; // allow changes all pins
		GPIO_PORTC_AFSEL_R |= 0x00; //disable alternative functions all pins
		GPIO_PORTC_DEN_R |= 0xFF; //set digital port 
		break;
		
		case PORT_D: 
		SET_BIT(RCGCGPIO,PIN_3); // enable clock 
		Delay(2); //waste time to make system stable
		GPIO_PORTD_LOCK_R = 0x4C4F434B;  // unlock CR 
		GPIO_PORTD_CR_R |= 0xFF; // allow changes all pins
		GPIO_PORTD_AFSEL_R |= 0x00; //disable alternative functions all pins
		GPIO_PORTD_DEN_R |= 0xFF; //set digital port 
		break;
		
		case PORT_E: 
		SET_BIT(RCGCGPIO,PIN_4); // enable clock 
		Delay(2); //waste time to make system stable
		GPIO_PORTE_LOCK_R = 0x4C4F434B;  // unlock CR 
		GPIO_PORTE_CR_R |= 0xFF; // allow changes all pins
		GPIO_PORTE_AFSEL_R |= 0x00; //disable alternative functions all pins
		GPIO_PORTE_DEN_R |= 0xFF; //set digital port 
		break;
		
		case PORT_F: 
		SET_BIT(RCGCGPIO,PIN_5); // enable clock 
		Delay(2); //waste time to make system stable
		GPIO_PORTF_LOCK_R = 0x4C4F434B;  // unlock CR 
		GPIO_PORTF_CR_R |= 0xFF; // allow changes all pins
		GPIO_PORTF_AFSEL_R |= 0x00; //disable alternative functions all pins
		GPIO_PORTF_DEN_R |= 0xFF; //set digital port 
		break;
	}
}

void GPIO_VoidSetPortDir(u8 copy_u8PORT, u8 copy_u8Direction)
{
	switch(copy_u8PORT)
	{
		case PORT_A: GPIO_PORTA_DIR_R |= copy_u8Direction; break;
		case PORT_B: GPIO_PORTB_DIR_R |= copy_u8Direction; break;
		case PORT_C: GPIO_PORTC_DIR_R |= copy_u8Direction; break;
		case PORT_D: GPIO_PORTD_DIR_R |= copy_u8Direction; break;
		case PORT_E: GPIO_PORTE_DIR_R |= copy_u8Direction; break;
		case PORT_F: GPIO_PORTF_DIR_R |= copy_u8Direction; break;
	}
}

void GPIO_VoidSetPinDir(u8 copy_u8PORT,u8 copy_u8PIN,u8 copy_u8Direction)
{
	if (copy_u8Direction == OUTPUT_PIN)
	{
		switch(copy_u8PORT)
		{
			case PORT_A: SET_BIT(GPIO_PORTA_DIR_R,copy_u8PIN); break;
			case PORT_B: SET_BIT(GPIO_PORTB_DIR_R,copy_u8PIN); break;
			case PORT_C: SET_BIT(GPIO_PORTC_DIR_R,copy_u8PIN); break;
			case PORT_D: SET_BIT(GPIO_PORTD_DIR_R,copy_u8PIN); break;
			case PORT_E: SET_BIT(GPIO_PORTE_DIR_R,copy_u8PIN); break;
			case PORT_F: SET_BIT(GPIO_PORTF_DIR_R,copy_u8PIN); break;
		}
	}
	else if (copy_u8Direction == INPUT_PIN)
	{
		switch(copy_u8PORT)
		{
			case PORT_A: CLR_BIT(GPIO_PORTA_DIR_R,copy_u8PIN); break;
			case PORT_B: CLR_BIT(GPIO_PORTB_DIR_R,copy_u8PIN); break;
			case PORT_C: CLR_BIT(GPIO_PORTC_DIR_R,copy_u8PIN); break;
			case PORT_D: CLR_BIT(GPIO_PORTD_DIR_R,copy_u8PIN); break;
			case PORT_E: CLR_BIT(GPIO_PORTE_DIR_R,copy_u8PIN); break;
			case PORT_F: CLR_BIT(GPIO_PORTF_DIR_R,copy_u8PIN); break;
		}
	}
}

void GPIO_VoidSetPinPullUp(u8 copy_u8PORT, u8 copy_u8PIN)
{
	switch(copy_u8PORT)
	{
		case PORT_A: SET_BIT(GPIO_PORTA_PUR_R,copy_u8PIN); break;
		case PORT_B: SET_BIT(GPIO_PORTB_PUR_R,copy_u8PIN); break;
		case PORT_C: SET_BIT(GPIO_PORTC_PUR_R,copy_u8PIN); break;
		case PORT_D: SET_BIT(GPIO_PORTD_PUR_R,copy_u8PIN); break;
		case PORT_E: SET_BIT(GPIO_PORTE_PUR_R,copy_u8PIN); break;
		case PORT_F: SET_BIT(GPIO_PORTF_PUR_R,copy_u8PIN); break;
	}
}

void GPIO_VoidSetPortValue(u8 copy_u8PORT,u8 copy_u8Value)
{
	switch(copy_u8PORT)
	{
		case PORT_A: GPIO_PORTA_DATA_R &=0xFFFFFF00; GPIO_PORTA_DATA_R |= copy_u8Value; break;
		case PORT_B: GPIO_PORTB_DATA_R &=0xFFFFFF00; GPIO_PORTB_DATA_R |= copy_u8Value; break;
		case PORT_C: GPIO_PORTC_DATA_R &=0xFFFFFF00; GPIO_PORTC_DATA_R |= copy_u8Value; break;
		case PORT_D: GPIO_PORTD_DATA_R &=0xFFFFFF00; GPIO_PORTD_DATA_R |= copy_u8Value; break;
		case PORT_E: GPIO_PORTE_DATA_R &=0xFFFFFF00; GPIO_PORTE_DATA_R |= copy_u8Value; break;
		case PORT_F: GPIO_PORTF_DATA_R &=0xFFFFFF00; GPIO_PORTF_DATA_R |= copy_u8Value; break;
	}
}

void GPIO_VoidSetPinValue(u8 copy_u8PORT,u8 copy_u8PIN,u8 copy_u8Value)
{
	if (copy_u8Value == HIGH)
	{
		switch(copy_u8PORT)
		{
			case PORT_A: SET_BIT(GPIO_PORTA_DATA_R,copy_u8PIN); break;
			case PORT_B: SET_BIT(GPIO_PORTB_DATA_R,copy_u8PIN); break;
			case PORT_C: SET_BIT(GPIO_PORTC_DATA_R,copy_u8PIN); break;
			case PORT_D: SET_BIT(GPIO_PORTD_DATA_R,copy_u8PIN); break;
			case PORT_E: SET_BIT(GPIO_PORTE_DATA_R,copy_u8PIN); break;
			case PORT_F: SET_BIT(GPIO_PORTF_DATA_R,copy_u8PIN); break;
		}
	}
	else if (copy_u8Value == LOW)
	{
		switch(copy_u8PORT)
		{
			case PORT_A: CLR_BIT(GPIO_PORTA_DATA_R,copy_u8PIN); break;
			case PORT_B: CLR_BIT(GPIO_PORTB_DATA_R,copy_u8PIN); break;
			case PORT_C: CLR_BIT(GPIO_PORTC_DATA_R,copy_u8PIN); break;
			case PORT_D: CLR_BIT(GPIO_PORTD_DATA_R,copy_u8PIN); break;
			case PORT_E: CLR_BIT(GPIO_PORTE_DATA_R,copy_u8PIN); break;
			case PORT_F: CLR_BIT(GPIO_PORTF_DATA_R,copy_u8PIN); break;
		}
	}
}

u8 GPIO_U8GetPinValue(u8 copy_u8PORT,u8 copy_u8PIN)
{
	u8 local_u8RET;
	switch(copy_u8PORT)
	{
		case PORT_A: local_u8RET= GET_BIT(GPIO_PORTA_DATA_R,copy_u8PIN); break;
		case PORT_B: local_u8RET= GET_BIT(GPIO_PORTB_DATA_R,copy_u8PIN); break;
		case PORT_C: local_u8RET= GET_BIT(GPIO_PORTC_DATA_R,copy_u8PIN); break;
		case PORT_D: local_u8RET= GET_BIT(GPIO_PORTD_DATA_R,copy_u8PIN); break;
		case PORT_E: local_u8RET= GET_BIT(GPIO_PORTE_DATA_R,copy_u8PIN); break;
		case PORT_F: local_u8RET= GET_BIT(GPIO_PORTF_DATA_R,copy_u8PIN); break;
	}
	return local_u8RET;
}

























