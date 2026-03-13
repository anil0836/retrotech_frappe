import frappe

def override_relative_time(bootinfo):
    bootinfo.disable_relative_time = True
