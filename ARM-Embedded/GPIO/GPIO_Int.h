/***************************************************************/
/*  Author 	     : Hashim Sobhi                               **/
/*  Date    	 : 23.3.2022                                  **/
/*  Description  : GPIO driver 	                	          **/
/*  Version 	 : 1.0                                        **/
/***************************************************************/
#ifndef _GPIO_INT_H_
#define _GPIO_INT_H_

// PORT NUM
#define PORT_A 0
#define PORT_B 1
#define PORT_C 2
#define PORT_D 3
#define PORT_E 4
#define PORT_F 5

// PIN NUM
#define PIN_0 0
#define PIN_1 1
#define PIN_2 2
#define PIN_3 3
#define PIN_4 4
#define PIN_5 5
#define PIN_6 6
#define PIN_7 7

// DIRECTION VALUE
#define OUTPUT_PORT 0xFF
#define INPUT_PORT  0x00
#define OUTPUT_PIN  1
#define INPUT_PIN   0

// PIN VALUE
#define HIGH 1
#define LOW  0


void GPIO_VoidEnablePort(u8 copy_U8port);
void GPIO_VoidSetPortDir(u8 copy_u8port, u8 copy_u8Direction);
void GPIO_VoidSetPinDir(u8 copy_u8PORT,u8 copy_u8PIN,u8 copy_u8Direction);
void GPIO_VoidSetPinPullUp(u8 copy_u8PORT, u8 copy_u8PIN);
void GPIO_VoidSetPortValue(u8 copy_u8PORT,u8 copy_u8Value);
void GPIO_VoidSetPinValue(u8 copy_u8PORT,u8 copy_u8PIN,u8 copy_u8Value);
u8 GPIO_U8GetPinValue(u8 copy_u8PORT,u8 copy_u8PIN);

#endif