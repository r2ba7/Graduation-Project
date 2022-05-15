/***************************************************************/
/*  Author 	     : Hashim Sobhi                               **/
/*  Date    	 : 25.3.2022                                  **/
/*  Description  : UART0 driver 	              	          **/
/*  Version 	 : 1.0                                        **/
/***************************************************************/
#include "STD_TYPES.h"
#include "BIT_MATHS.h"
#include "UART_Int.h"
#include "Reg.h"

#define F_CLK 20000000

void UART0_VoidInit(u32 copy_u8baudRate)
{
	f32 temp;
	// enable uart0 clock
	SET_BIT(RCGCUART ,BIT_0);
	// enable AF bit0,1 
	SET_BIT(GPIO_PORTA_AFSEL_R ,BIT_0);	
	SET_BIT(GPIO_PORTA_AFSEL_R ,BIT_1);
	// assign uart signal to bits0,1
	SET_BIT(GPIO_PORTA_PCTL_R,BIT_0);
	SET_BIT(GPIO_PORTA_PCTL_R,BIT_4);
	//disable uart
	CLR_BIT(UARTCTL,UARTEN);
	// baud rate 
	temp = (F_CLK / (f32)(16*copy_u8baudRate)) - (u32)(F_CLK / (16*copy_u8baudRate));
	UARTIBRD = (u32)(F_CLK / (16*copy_u8baudRate));
	UARTFBRD = (u32)(64 * temp + 0.5);
	// set data 8 bits
	SET_BIT(UARTLCRH,WLEN0);
	SET_BIT(UARTLCRH,WLEN1);
	// clear FIFO
	CLR_BIT(UARTLCRH,FEN);
	//rx enable 
	SET_BIT(UARTCTL,RXE);
	//tx enable 
	SET_BIT(UARTCTL,TXE);
	//enable uart
	SET_BIT(UARTCTL,UARTEN);
}

void UART0_VoidSendChr(u8 copy_u8Chr)
{
	while (GET_BIT(UARTFR,TXFF)); //wait until tx buffer not full
	UARTDR = copy_u8Chr;
}
void UART0_VoidSendString(u8* copy_u8str)
{
	u16 loc_u8counter = 0;
	while (copy_u8str[loc_u8counter]!='\0')
	{
		UART0_VoidSendChr(copy_u8str[loc_u8counter]);
		loc_u8counter++;
	}
}
u8 UART0_U8GetData(void)
{
	while (GET_BIT(UARTFR,RXFE)); //wait data to receive
	return ((u8)(UARTDR&0xFF));
}

void UART0_ReadString(u8* copy_u8str)
{
	u8 c =1;
	u32 i = 0;
	while(c != (u8)TERMINATE_STRING)
	{
		c = UART0_U8GetData();
		copy_u8str[i++] = c;
	}
	copy_u8str[i] = 0 ;
}
void UART0_VoidSendNum(u32 copy_u32num)
{
	if (copy_u32num == 0)
	{
		UART0_VoidSendChr('0');
	}
	else
	{
		u8 local_u8num = 0;
		u32 local_u32rev = 1;
		while (copy_u32num != 0)
		{
			local_u32rev = (local_u32rev*10)+(copy_u32num%10);
			copy_u32num /= 10;
		}
		while (local_u32rev != 1)
		{
			local_u8num = local_u32rev%10;
			local_u32rev /= 10;
			UART0_VoidSendChr(local_u8num+48);
		} 	
	}	
}
void UART0_VoidEnRxInterrpt(void)
{
	// enable interrupt
	SET_BIT(UARTIM,RXIM);
	SET_BIT(NVIC_EN0,BIT_5);
}

