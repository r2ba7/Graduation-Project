/***************************************************************/
/*  Author 	     : Hashim Sobhi                               **/
/*  Date    	 : 25.3.2022                                  **/
/*  Description  : UART driver 	                	          **/
/*  Version 	 : 1.0                                        **/
/***************************************************************/
#ifndef _UART_INT_H_
#define _UART_INT_H_

/*UARTCTL pins*/
#define UARTEN 0
#define TXE    8
#define RXE    9
/*UARTLCRH pins*/
#define FEN   4
#define WLEN0 5
#define WLEN1 6
/*UARTFR pins*/
#define RXFE 4
#define TXFF 5
#define RXFF 6
#define TXFE 7
/*UARTIM pins*/
#define RXIM 4

#define TERMINATE_STRING '\r'

void UART0_VoidInit(u32 copy_u8baudRate);
void UART0_VoidSendChr(u8 copy_u8Chr);
u8 UART0_U8GetData(void);
void UART0_ReadString(u8* copy_u8str);
void UART0_VoidSendString(u8* copy_u8str);
void UART0_VoidSendNum(u32 copy_u32num);
void UART0_VoidEnRxInterrpt(void);
void UART0_VoidEnRxInterrpt(void);
#endif