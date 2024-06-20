package com.macro.mall.tiny.modules.epaper.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.macro.mall.tiny.common.api.CommonPage;
import com.macro.mall.tiny.common.api.CommonResult;
import com.macro.mall.tiny.modules.epaper.model.EpaperPic;
import com.macro.mall.tiny.modules.epaper.service.impl.EpaperPicServiceImpl;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

/**
 * <p>
 * 电子日历管理 前端控制器
 * </p>
 * 查看历史生成的图片，自动生成明天的图片
 *
 * @author Ymri
 * @since 2024-04-06
 */
@RestController
@RequestMapping("/epaper/epaperPic")
public class EpaperPicController {


    @Resource
    private EpaperPicServiceImpl epaperPicService;

    @Operation(summary = "根据用户分页获取日历列表")
    @RequestMapping(value = "/list", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<CommonPage<EpaperPic>> list(
            @RequestParam(value = "pageSize", defaultValue = "5") Integer pageSize,
            @RequestParam(value = "pageNum", defaultValue = "1") Integer pageNum) {
        Page<EpaperPic> epaperPicPage = epaperPicService.list(pageSize, pageNum);
        return CommonResult.success(CommonPage.restPage(epaperPicPage));
    }

    @Operation(summary = "获得用户能够查看的日历列表")
    @RequestMapping(value = "/allList", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult findAlllist(String date) {

        List<EpaperPic> epaperPicPage = epaperPicService.listByDate(date);
        return CommonResult.success(epaperPicPage);
    }

    @Operation(summary = "删除已经生成好的日历图")
    @RequestMapping(value = "/delete/{id}", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult delete(@PathVariable Integer id) {
        boolean success = epaperPicService.delete(id);
        if (success) {
            return CommonResult.success(null);
        }
        return CommonResult.failed();
    }


}
