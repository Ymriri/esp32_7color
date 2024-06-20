package com.macro.mall.tiny.modules.epaper.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.macro.mall.tiny.common.api.CommonPage;
import com.macro.mall.tiny.common.api.CommonResult;
import com.macro.mall.tiny.modules.epaper.dto.EpaperPicBindUserDto;
import com.macro.mall.tiny.modules.epaper.model.EpaperOriginal;
import com.macro.mall.tiny.modules.epaper.service.impl.EpaperOriginalServiceImpl;
import com.macro.mall.tiny.modules.ums.model.UmsAdmin;
import io.swagger.v3.oas.annotations.Operation;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

/**
 * <p>
 * 前端控制器
 * </p>
 *
 * @author Ymri
 * @since 2024-04-06
 */
@RestController
@RequestMapping("/epaper/epaperOriginal")
public class EpaperOriginalController {

    @Resource
    private EpaperOriginalServiceImpl epaperOriginalService;


    @Operation(summary = "根据用户分页获取用户列表")
    @RequestMapping(value = "/list", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<CommonPage<EpaperOriginal>> list(@RequestParam(value = "keyword", required = false) String keyword, @RequestParam(value = "pageSize", defaultValue = "5") Integer pageSize, @RequestParam(value = "pageNum", defaultValue = "1") Integer pageNum) {
        Page<EpaperOriginal> epaperOriginalPage = epaperOriginalService.list(keyword, pageSize, pageNum);
        return CommonResult.success(CommonPage.restPage(epaperOriginalPage));
    }


    // 输入接口
    @Operation(summary = "添加数据")
    @RequestMapping(value = "/create", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult create(@RequestBody EpaperOriginal epaperOriginal) {
        EpaperOriginal original = epaperOriginalService.create(epaperOriginal);
        if (original != null) {
            return CommonResult.success(epaperOriginal);
        }
        return CommonResult.failed();
    }

    @Operation(summary = "删除数据")
    @RequestMapping(value = "/delete/{id}", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult delete(@PathVariable Integer id) {
        boolean success = epaperOriginalService.delete(id);
        if (success) {
            return CommonResult.success(null);
        }
        return CommonResult.failed();
    }

    @Operation(summary = "获得能够推送的用户")
    @RequestMapping(value = "/push", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult getPush() {
        List<UmsAdmin> pushUserList = epaperOriginalService.getPushUser();
        return CommonResult.success(pushUserList);
    }

    @Operation(summary = "查看原图")
    @RequestMapping(value = "/pic/{id}", method = RequestMethod.GET, headers = "Accept=application/json")
    public void showPic(@PathVariable Integer id, HttpServletResponse response) {
        epaperOriginalService.showPic(id, response);
    }

    @Operation(summary = "预览图")
    @RequestMapping(value = "/pic/out/{id}", method = RequestMethod.GET, headers = "Accept=application/json")
    public void showOutPic(@PathVariable Integer id, HttpServletResponse response) {
        epaperOriginalService.showOutPic(id, response);
    }

    @Operation(summary = "根据ID获取资源详情")
    @RequestMapping(value = "/pic/user/{file}", method = RequestMethod.GET, headers = "Accept=application/json")
    public void showOutPic(@PathVariable String file, HttpServletResponse response) {
        epaperOriginalService.showUserPic(file, response);
    }

    @Operation(summary = "设置给用户推送")
    @RequestMapping(value = "/push", method = RequestMethod.POST)
    public CommonResult pushUser(@RequestBody EpaperPicBindUserDto epaperPicBindUserDto) {
        boolean success = epaperOriginalService.createPicBindUser(epaperPicBindUserDto);
        if (success) {
            return CommonResult.success(null);
        } else {
            return CommonResult.failed();
        }
    }

    // 先插入，再上传图片...

    @RequestMapping(value = "/upload/{id}", method = RequestMethod.POST)
    public CommonResult uploadPic(@PathVariable Integer id, MultipartFile img) {
        if (epaperOriginalService.uploadPic(id, img)) {
            return CommonResult.success(null);
        }
        return CommonResult.failed();
    }


}
