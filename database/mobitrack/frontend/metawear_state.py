from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from mbientlab.metawear.cbindings import *
from threading import Event
from sys import argv
import os
import time
import numpy as np

from frontend.mobitrack import Mobitrack

class State:
  def __init__(self, device, mobitrack):
      self.device = device
      self.callback = cbindings.FnVoid_VoidP_DataP(self.data_handler)
      self.processor = None
      self.mobitrack = mobitrack

  def data_handler(self, ctx, data):
      values = parse_value(data, n_elem=2)
      time_stamp = data.contents.epoch
      status = self.mobitrack.processStep(np.array([time_stamp / 1000,  values[0].x, values[0].y, values[0].z, values[1].x, values[1].y, values[1].z]))

      if status["isRep"] != -1: self.led_on(LedColor.BLUE, 0.3)

  def setup(self):
      libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 6000)
      time.sleep(1.5)

      e = Event()

      def processor_created(context, pointer):
          self.processor = pointer
          e.set()

      fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)

      acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.device.board)
      gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.device.board)

      signals = (c_void_p * 1)()
      signals[0] = gyro
      libmetawear.mbl_mw_dataprocessor_fuser_create(acc, signals, 1, None, fn_wrapper)
      e.wait()
      libmetawear.mbl_mw_datasignal_subscribe(self.processor, None, self.callback)

  def start(self):
      self.led_on(LedColor.GREEN, 2)
      libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.device.board)
      libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.device.board)

      libmetawear.mbl_mw_gyro_bmi160_start(self.device.board)
      libmetawear.mbl_mw_acc_start(self.device.board)

  def led_on(self, color, duration, clear=True):
    pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
    libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.SOLID)
    libmetawear.mbl_mw_led_write_pattern(self.device.board, byref(pattern), color)
    libmetawear.mbl_mw_led_play(self.device.board)
    time.sleep(duration)
    if clear: libmetawear.mbl_mw_led_stop_and_clear(self.device.board)