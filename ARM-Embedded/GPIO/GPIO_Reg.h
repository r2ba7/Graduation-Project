/***************************************************************/
/*  Author 	     : Hashim Sobhi                               **/
/*  Date    	 : 23.3.2022                                  **/
/*  Description  : GPIO driver 	                	          **/
/*  Version 	 : 1.0                                        **/
/***************************************************************/
#ifndef _GPIO_REG_H_
#define _GPIO_REG_H_

#define RCGCGPIO *((volatile u32*)0x400FE608) //clock enable 

// data registers
#define GPIO_PORTA_DATA_R *((volatile u32*)0x400043FC)
#define GPIO_PORTB_DATA_R *((volatile u32*)0x400053FC)
#define GPIO_PORTC_DATA_R *((volatile u32*)0x400063FC)
#define GPIO_PORTD_DATA_R *((volatile u32*)0x400073FC)
#define GPIO_PORTE_DATA_R *((volatile u32*)0x400243FC)
#define GPIO_PORTF_DATA_R *((volatile u32*)0x400253FC)
// direction register
#define GPIO_PORTA_DIR_R *((volatile u32*)0x40004400)
#define GPIO_PORTB_DIR_R *((volatile u32*)0x40005400)
#define GPIO_PORTC_DIR_R *((volatile u32*)0x40006400)
#define GPIO_PORTD_DIR_R *((volatile u32*)0x40007400)
#define GPIO_PORTE_DIR_R *((volatile u32*)0x40024400)
#define GPIO_PORTF_DIR_R *((volatile u32*)0x40025400)
// alternative function selection
#define GPIO_PORTA_AFSEL_R *((volatile u32*)0x40004420)
#define GPIO_PORTB_AFSEL_R *((volatile u32*)0x40005420)
#define GPIO_PORTC_AFSEL_R *((volatile u32*)0x40006420)
#define GPIO_PORTD_AFSEL_R *((volatile u32*)0x40007420)
#define GPIO_PORTE_AFSEL_R *((volatile u32*)0x40024420)
#define GPIO_PORTF_AFSEL_R *((volatile u32*)0x40025420)
// pull up enable
#define GPIO_PORTA_PUR_R *((volatile u32*)0x40004510)
#define GPIO_PORTB_PUR_R *((volatile u32*)0x40005510)
#define GPIO_PORTC_PUR_R *((volatile u32*)0x40006510)
#define GPIO_PORTD_PUR_R *((volatile u32*)0x40007510)
#define GPIO_PORTE_PUR_R *((volatile u32*)0x40024510)
#define GPIO_PORTF_PUR_R *((volatile u32*)0x40025510)
// digital pins enable
#define GPIO_PORTA_DEN_R *((volatile u32*)0x4000451C)
#define GPIO_PORTB_DEN_R *((volatile u32*)0x4000551C)
#define GPIO_PORTC_DEN_R *((volatile u32*)0x4000651C)
#define GPIO_PORTD_DEN_R *((volatile u32*)0x4000751C)
#define GPIO_PORTE_DEN_R *((volatile u32*)0x4002451C)
#define GPIO_PORTF_DEN_R *((volatile u32*)0x4002551C)
// write 0x4C4F434B to unlock 
#define GPIO_PORTA_LOCK_R *((volatile u32*)0x40004520)
#define GPIO_PORTB_LOCK_R *((volatile u32*)0x40005520)
#define GPIO_PORTC_LOCK_R *((volatile u32*)0x40006520)
#define GPIO_PORTD_LOCK_R *((volatile u32*)0x40007520)
#define GPIO_PORTE_LOCK_R *((volatile u32*)0x40024520)
#define GPIO_PORTF_LOCK_R *((volatile u32*)0x40025520)
// commit register
#define GPIO_PORTA_CR_R *((volatile u32*)0x40004524)
#define GPIO_PORTB_CR_R *((volatile u32*)0x40005524)
#define GPIO_PORTC_CR_R *((volatile u32*)0x40006524)
#define GPIO_PORTD_CR_R *((volatile u32*)0x40007524)
#define GPIO_PORTE_CR_R *((volatile u32*)0x40024524)
#define GPIO_PORTF_CR_R *((volatile u32*)0x40025524)
// analog mode enable
#define GPIO_PORTA_AMSEL_R *((volatile u32*)0x40004528)
#define GPIO_PORTB_AMSEL_R *((volatile u32*)0x40005528)
#define GPIO_PORTC_AMSEL_R *((volatile u32*)0x40006528)
#define GPIO_PORTD_AMSEL_R *((volatile u32*)0x40007528)
#define GPIO_PORTE_AMSEL_R *((volatile u32*)0x40024528)
#define GPIO_PORTF_AMSEL_R *((volatile u32*)0x40025528)
// port control register
#define GPIO_PORTA_PCTL_R *((volatile u32*)0x4000452C)
#define GPIO_PORTB_PCTL_R *((volatile u32*)0x4000552C)
#define GPIO_PORTC_PCTL_R *((volatile u32*)0x4000652C)
#define GPIO_PORTD_PCTL_R *((volatile u32*)0x4000752C)
#define GPIO_PORTE_PCTL_R *((volatile u32*)0x4002452C)
#define GPIO_PORTF_PCTL_R *((volatile u32*)0x4002552C)
// ADC control register
#define GPIO_PORTA_ADCCTL_R *((volatile u32*)0x40004530)
#define GPIO_PORTB_ADCCTL_R *((volatile u32*)0x40005530)
#define GPIO_PORTC_ADCCTL_R *((volatile u32*)0x40006530)
#define GPIO_PORTD_ADCCTL_R *((volatile u32*)0x40007530)
#define GPIO_PORTE_ADCCTL_R *((volatile u32*)0x40024530)
#define GPIO_PORTF_ADCCTL_R *((volatile u32*)0x40025530)


#endif