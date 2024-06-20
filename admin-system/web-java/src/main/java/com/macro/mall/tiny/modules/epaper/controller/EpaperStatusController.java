package com.macro.mall.tiny.modules.epaper.controller;

import com.macro.mall.tiny.common.api.CommonResult;
import com.macro.mall.tiny.modules.epaper.model.EpaperUserSetting;
import com.macro.mall.tiny.modules.epaper.service.EpaperHeartBeatService;
import jakarta.annotation.Resource;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

/**
 * @author Ymri
 * @version 1.0
 * @since 2024/6/14 09:33
 * EpaperStatus
 */
@RestController
@RequestMapping("/epaper/Estatus")
public class EpaperStatusController {

    private static final Logger LOGGER = LoggerFactory.getLogger(EpaperStatusController.class);

    @Resource
    private EpaperHeartBeatService epaperHeartBeatService;

    /**
     * 设备心跳
     *
     * @param id
     * @param ip
     * @return
     */
    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public String helloHeaertBeat(@PathVariable Long id, String ip) {
        LOGGER.info("inif_epaper");
        // 返回需要连接的wifi信息
        EpaperUserSetting userSetting = epaperHeartBeatService.keepHeaertBeat(id, ip);
        LOGGER.info(userSetting.toString());
        return userSetting.getWifiSsid() + ":" + userSetting.getWifiPassword();
    }

    /**
     * 设备心跳 返回魔法数字
     *
     * @param id
     * @param ip
     * @return
     */
    @RequestMapping(value = "/heartbeat/{id}", method = RequestMethod.GET)
    public String keepHeaertBeat(@PathVariable Long id, String ip) {
        LOGGER.info("keepHeaertBeat");
        // 更新心跳时间
        epaperHeartBeatService.keepHeaertBeat(id, ip);
        // 返回魔法数字
        return epaperHeartBeatService.getEPaper(id);
    }

    /**
     * 获得当天的Epaper信息
     * @param id
     * @param response
     */
    @RequestMapping(value = "/bin/{id}", method = RequestMethod.GET)
    public void getBindUser(@PathVariable Long id, HttpServletResponse response) {
        // 获取绑定用户
        // 检查用户
        epaperHeartBeatService.getBinData(id, response);
    }

    @GetMapping("/echo")
    public CommonResult<String> echo(String msg) {
        LOGGER.info("echo" + msg);
        return CommonResult.success("echo");
    }
}
