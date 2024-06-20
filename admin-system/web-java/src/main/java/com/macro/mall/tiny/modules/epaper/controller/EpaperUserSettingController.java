package com.macro.mall.tiny.modules.epaper.controller;

import com.macro.mall.tiny.common.api.CommonResult;
import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import com.macro.mall.tiny.modules.epaper.service.impl.EpaperUserSettingServiceImpl;
import com.macro.mall.tiny.modules.ums.model.UmsAdmin;
import io.swagger.v3.oas.annotations.Operation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * <p>
 * 用户设置 前端控制器
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@RestController
@RequestMapping("/epaper/epaperUserSetting")
public class EpaperUserSettingController {

    @Autowired
    private EpaperUserSettingServiceImpl epaperUserSettingService;


    @Operation(summary = "查找指定用户信息")
    @GetMapping(value = "/get")
    @ResponseBody
    public CommonResult get() {
        EpaperUserSetting epaperUserSetting = epaperUserSettingService.getEpaperUserSetting();

        return CommonResult.success(epaperUserSetting);
    }

    @Operation(summary = "修改指定用户信息")
    @RequestMapping(value = "/update/{id}", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult update(@PathVariable Long id, @RequestBody EpaperUserSetting epaperUserSetting) {
        boolean success = epaperUserSettingService.updateEpaperUserSetting(epaperUserSetting);
        if (success) {
            return CommonResult.success(null);
        }
        return CommonResult.failed();
    }

}
